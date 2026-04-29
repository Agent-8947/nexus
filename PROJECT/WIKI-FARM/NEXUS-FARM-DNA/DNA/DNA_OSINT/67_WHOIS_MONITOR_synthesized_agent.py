#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: WHOIS_MONITOR
Tier: S-Target (Production-Hardened)

Queries domain registration data via RDAP (Registration Data Access Protocol),
the modern standardized replacement for legacy WHOIS.
Uses IANA bootstrap to find the correct RDAP server for any TLD.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("WHOIS_MONITOR")

RDAP_BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
MAX_RETRIES = 3
RETRY_BACKOFF = 1.5


@dataclass
class WhoisRecord:
    domain: str
    registrar: str = ""
    registration_date: str = ""
    expiration_date: str = ""
    last_updated: str = ""
    status: list[str] = field(default_factory=list)
    nameservers: list[str] = field(default_factory=list)
    registrant_name: str = ""
    registrant_org: str = ""


@dataclass
class WhoisReport:
    targets: list[WhoisRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class WhoisMonitorAgent:
    """RDAP-based WHOIS lookup with IANA bootstrap resolution."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "NEXUS-OSINT/1.0",
            "Accept": "application/rdap+json",
        })
        self._rdap_cache: dict[str, str] = {}
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS whois_records (
                        id                INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain            TEXT NOT NULL,
                        registrar         TEXT,
                        registration_date TEXT,
                        expiration_date   TEXT,
                        last_updated      TEXT,
                        status            TEXT,
                        nameservers       TEXT,
                        data_hash         TEXT NOT NULL,
                        ts                DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(domain, data_hash)
                    )
                """)
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _api_get(self, url: str) -> Optional[dict]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d for %s", attempt, MAX_RETRIES, url)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Request error for %s: %s", url, exc)
                return None
        return None

    def _resolve_rdap_server(self, domain: str) -> Optional[str]:
        """Resolve the correct RDAP server for a domain's TLD via IANA bootstrap."""
        tld = domain.rsplit(".", 1)[-1].lower()

        if tld in self._rdap_cache:
            return self._rdap_cache[tld]

        bootstrap = self._api_get(RDAP_BOOTSTRAP_URL)
        if bootstrap is None:
            logger.error("Failed to fetch IANA RDAP bootstrap")
            return None

        for service in bootstrap.get("services", []):
            tlds, urls = service
            if tld in tlds and urls:
                base = urls[0].rstrip("/")
                self._rdap_cache[tld] = base
                return base

        logger.warning("No RDAP server found for TLD: %s", tld)
        return None

    def _extract_events(self, events: list[dict]) -> dict[str, str]:
        """Extract registration/expiration/update dates from RDAP events."""
        result: dict[str, str] = {}
        for ev in events:
            action = ev.get("eventAction", "")
            date = ev.get("eventDate", "")
            if action == "registration":
                result["registration_date"] = date
            elif action == "expiration":
                result["expiration_date"] = date
            elif action == "last changed":
                result["last_updated"] = date
        return result

    def _extract_entity_info(self, entities: list[dict]) -> dict[str, str]:
        """Extract registrant name/org from RDAP entities."""
        info: dict[str, str] = {}
        for entity in entities:
            roles = entity.get("roles", [])
            if "registrant" in roles:
                vcard = entity.get("vcardArray", [None, []])
                if len(vcard) > 1:
                    for prop in vcard[1]:
                        if prop[0] == "fn":
                            info["registrant_name"] = prop[3]
                        elif prop[0] == "org":
                            info["registrant_org"] = prop[3]
            if "registrar" in roles:
                vcard = entity.get("vcardArray", [None, []])
                if len(vcard) > 1:
                    for prop in vcard[1]:
                        if prop[0] == "fn":
                            info["registrar"] = prop[3]
        return info

    def lookup(self, domain: str) -> WhoisRecord:
        """Full RDAP lookup for a single domain."""
        logger.info("RDAP lookup for: %s", domain)
        record = WhoisRecord(domain=domain)

        rdap_base = self._resolve_rdap_server(domain)
        if rdap_base is None:
            return record

        data = self._api_get(f"{rdap_base}/domain/{domain}")
        if data is None:
            logger.warning("No RDAP data for %s", domain)
            return record

        # Status
        record.status = data.get("status", [])

        # Nameservers
        for ns in data.get("nameservers", []):
            name = ns.get("ldhName", "")
            if name:
                record.nameservers.append(name.lower())

        # Events (dates)
        events = self._extract_events(data.get("events", []))
        record.registration_date = events.get("registration_date", "")
        record.expiration_date = events.get("expiration_date", "")
        record.last_updated = events.get("last_updated", "")

        # Entities (registrant, registrar)
        entity_info = self._extract_entity_info(data.get("entities", []))
        record.registrar = entity_info.get("registrar", "")
        record.registrant_name = entity_info.get("registrant_name", "")
        record.registrant_org = entity_info.get("registrant_org", "")

        return record

    def execute_scan(self, *domains: str) -> WhoisReport:
        report = WhoisReport()

        for domain in domains:
            try:
                rec = self.lookup(domain)
                report.targets.append(rec)
            except Exception as exc:
                logger.error("Failed lookup for %s: %s", domain, exc)
                report.errors.append(f"{domain}: {exc}")

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in report.targets:
                    snapshot = json.dumps(asdict(rec), sort_keys=True)
                    conn.execute(
                        """INSERT OR IGNORE INTO whois_records
                           (domain, registrar, registration_date, expiration_date,
                            last_updated, status, nameservers, data_hash)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (rec.domain, rec.registrar, rec.registration_date,
                         rec.expiration_date, rec.last_updated,
                         json.dumps(rec.status), json.dumps(rec.nameservers),
                         self._hash(snapshot)),
                    )
                conn.commit()
            logger.info("Persisted %d WHOIS records", len(report.targets))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 67_WHOIS_MONITOR_synthesized_agent.py <domain1> [domain2] ...")
        sys.exit(1)

    agent = WhoisMonitorAgent()
    result = agent.execute_scan(*sys.argv[1:])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
