#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: CERTIFICATE_TRANSPARENCY
Tier: S-Target (Production-Hardened)

Queries crt.sh for SSL/TLS certificate history. Parses issuer, validity dates,
SANs (Subject Alternative Names), and detects wildcard certs.
Stores full structured data, not just hashes.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("CERTIFICATE_TRANSPARENCY")

CRT_SH_URL = "https://crt.sh/"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class CertRecord:
    serial_number: str
    issuer_name: str
    common_name: str
    san_names: list[str] = field(default_factory=list)
    not_before: str = ""
    not_after: str = ""
    is_wildcard: bool = False
    is_expired: bool = False


@dataclass
class CertTransparencyReport:
    target: str
    total_certs: int = 0
    unique_issuers: int = 0
    wildcard_count: int = 0
    expired_count: int = 0
    certs: list[CertRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class CertificateTransparencyAgent:
    """Production CT log analyzer with structured cert metadata extraction."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cert_transparency (
                        id            INTEGER PRIMARY KEY AUTOINCREMENT,
                        target        TEXT NOT NULL,
                        serial_number TEXT NOT NULL,
                        issuer_name   TEXT,
                        common_name   TEXT,
                        san_names     TEXT,
                        not_before    TEXT,
                        not_after     TEXT,
                        is_wildcard   INTEGER DEFAULT 0,
                        is_expired    INTEGER DEFAULT 0,
                        data_hash     TEXT NOT NULL,
                        ts            DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(target, serial_number)
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

    def _fetch_ct_data(self, domain: str) -> Optional[list[dict]]:
        """Fetch CT log entries from crt.sh with retry."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(
                    CRT_SH_URL,
                    params={"q": domain, "output": "json"},
                    timeout=20,
                )
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d", attempt, MAX_RETRIES)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.JSONDecodeError as exc:
                logger.error("Invalid JSON: %s", exc)
                return None
            except requests.exceptions.RequestException as exc:
                logger.error("Network error: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    def _parse_cert(self, entry: dict) -> CertRecord:
        """Parse a single crt.sh JSON entry into structured CertRecord."""
        common_name = entry.get("common_name", "")
        name_value = entry.get("name_value", "")
        san_names = [s.strip() for s in name_value.split("\n") if s.strip()]
        not_before = entry.get("not_before", "")
        not_after = entry.get("not_after", "")

        is_wildcard = common_name.startswith("*.")
        is_expired = False
        if not_after:
            try:
                expiry = datetime.fromisoformat(not_after.replace("T", " ").split(".")[0])
                is_expired = expiry < datetime.now()
            except (ValueError, TypeError):
                pass

        return CertRecord(
            serial_number=str(entry.get("serial_number", entry.get("id", ""))),
            issuer_name=entry.get("issuer_name", ""),
            common_name=common_name,
            san_names=san_names,
            not_before=not_before,
            not_after=not_after,
            is_wildcard=is_wildcard,
            is_expired=is_expired,
        )

    def execute_scan(self, target: str) -> CertTransparencyReport:
        logger.info("Scanning CT logs for: %s", target)
        report = CertTransparencyReport(target=target)

        raw_data = self._fetch_ct_data(target)
        if raw_data is None:
            report.errors.append("Failed to fetch CT log data")
            return report

        # Deduplicate by serial number
        seen_serials: set[str] = set()
        issuers: set[str] = set()

        for entry in raw_data:
            cert = self._parse_cert(entry)
            if cert.serial_number in seen_serials:
                continue
            seen_serials.add(cert.serial_number)
            report.certs.append(cert)
            issuers.add(cert.issuer_name)
            if cert.is_wildcard:
                report.wildcard_count += 1
            if cert.is_expired:
                report.expired_count += 1

        report.total_certs = len(report.certs)
        report.unique_issuers = len(issuers)
        logger.info("Parsed %d unique certs, %d issuers, %d wildcards, %d expired",
                     report.total_certs, report.unique_issuers,
                     report.wildcard_count, report.expired_count)

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for cert in report.certs:
                    conn.execute(
                        """INSERT OR IGNORE INTO cert_transparency
                           (target, serial_number, issuer_name, common_name, san_names,
                            not_before, not_after, is_wildcard, is_expired, data_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (target, cert.serial_number, cert.issuer_name, cert.common_name,
                         json.dumps(cert.san_names), cert.not_before, cert.not_after,
                         int(cert.is_wildcard), int(cert.is_expired),
                         self._hash(f"{target}:{cert.serial_number}")),
                    )
                conn.commit()
            logger.info("Persisted %d cert records", report.total_certs)
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 66_CERTIFICATE_TRANSPARENCY_synthesized_agent.py <domain>")
        sys.exit(1)

    agent = CertificateTransparencyAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
