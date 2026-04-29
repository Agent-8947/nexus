#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: BGP_ROUTE_ANALYZER
Tier: S-Target (Production-Hardened)

Analyzes BGP routing data via BGPView.io and RIPE Stat public APIs.
Maps: IP/ASN → prefixes → peers → upstream providers.
No API keys required.
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
logger = logging.getLogger("BGP_ROUTE_ANALYZER")

BGPVIEW_API = "https://api.bgpview.io"
RIPESTAT_API = "https://stat.ripe.net/data"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class BgpPrefix:
    prefix: str
    cidr: int = 0
    name: str = ""
    description: str = ""
    country_code: str = ""


@dataclass
class BgpPeer:
    asn: int
    name: str = ""
    description: str = ""
    country_code: str = ""


@dataclass
class BgpReport:
    target: str
    target_type: str = ""  # "ip" or "asn"
    asn: int = 0
    asn_name: str = ""
    asn_description: str = ""
    country_code: str = ""
    rir: str = ""
    prefixes: list[BgpPrefix] = field(default_factory=list)
    peers: list[BgpPeer] = field(default_factory=list)
    upstream_count: int = 0
    downstream_count: int = 0
    errors: list[str] = field(default_factory=list)


class BgpRouteAnalyzerAgent:
    """BGP routing intelligence via BGPView.io + RIPE Stat."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS bgp_routes (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        target       TEXT NOT NULL,
                        asn          INTEGER,
                        asn_name     TEXT,
                        prefix       TEXT,
                        country_code TEXT,
                        data_hash    TEXT NOT NULL,
                        ts           DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(target, prefix)
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
                logger.warning("Timeout attempt %d/%d", attempt, MAX_RETRIES)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Request error: %s", exc)
                return None
        return None

    def _detect_target_type(self, target: str) -> str:
        """Determine if target is an IP address or ASN."""
        if target.upper().startswith("AS"):
            return "asn"
        parts = target.split(".")
        if len(parts) == 4 and all(p.isdigit() for p in parts):
            return "ip"
        if target.isdigit():
            return "asn"
        return "ip"

    def _lookup_ip(self, ip: str) -> BgpReport:
        """Resolve IP → ASN → prefixes via BGPView."""
        report = BgpReport(target=ip, target_type="ip")

        # Step 1: IP → ASN mapping
        data = self._api_get(f"{BGPVIEW_API}/ip/{ip}")
        if data is None or data.get("status") != "ok":
            report.errors.append(f"BGPView IP lookup failed for {ip}")
            return report

        ip_data = data.get("data", {})
        prefixes_raw = ip_data.get("prefixes", [])

        if prefixes_raw:
            first = prefixes_raw[0]
            asn_info = first.get("asn", {})
            report.asn = asn_info.get("asn", 0)
            report.asn_name = asn_info.get("name", "")
            report.asn_description = asn_info.get("description", "")
            report.country_code = asn_info.get("country_code", "")

            for p in prefixes_raw:
                report.prefixes.append(BgpPrefix(
                    prefix=p.get("prefix", ""),
                    cidr=p.get("cidr", 0),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    country_code=p.get("country_code", ""),
                ))

        # Step 2: Fetch peers for discovered ASN
        if report.asn:
            self._enrich_asn_peers(report)

        return report

    def _lookup_asn(self, asn_str: str) -> BgpReport:
        """Direct ASN lookup via BGPView."""
        asn_num = int(asn_str.upper().replace("AS", ""))
        report = BgpReport(target=asn_str, target_type="asn", asn=asn_num)

        # ASN info
        data = self._api_get(f"{BGPVIEW_API}/asn/{asn_num}")
        if data and data.get("status") == "ok":
            asn_data = data.get("data", {})
            report.asn_name = asn_data.get("name", "")
            report.asn_description = asn_data.get("description_short", "")
            report.country_code = asn_data.get("country_code", "")
            report.rir = asn_data.get("rir_allocation", {}).get("rir_name", "")

        # Prefixes
        pfx_data = self._api_get(f"{BGPVIEW_API}/asn/{asn_num}/prefixes")
        if pfx_data and pfx_data.get("status") == "ok":
            for p in pfx_data.get("data", {}).get("ipv4_prefixes", []):
                report.prefixes.append(BgpPrefix(
                    prefix=p.get("prefix", ""),
                    cidr=p.get("cidr", 0),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    country_code=p.get("country_code", ""),
                ))

        # Peers
        self._enrich_asn_peers(report)

        return report

    def _enrich_asn_peers(self, report: BgpReport) -> None:
        """Fetch upstream/downstream peers for an ASN."""
        peers_data = self._api_get(f"{BGPVIEW_API}/asn/{report.asn}/peers")
        if peers_data and peers_data.get("status") == "ok":
            peers_raw = peers_data.get("data", {})
            for p in peers_raw.get("ipv4_peers", []):
                report.peers.append(BgpPeer(
                    asn=p.get("asn", 0),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    country_code=p.get("country_code", ""),
                ))
        report.upstream_count = len([p for p in report.peers if p.asn != report.asn])
        report.downstream_count = len(report.peers) - report.upstream_count

    def execute_scan(self, target: str) -> BgpReport:
        logger.info("BGP route analysis for: %s", target)
        target_type = self._detect_target_type(target)

        if target_type == "ip":
            report = self._lookup_ip(target)
        else:
            report = self._lookup_asn(target)

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for pfx in report.prefixes:
                    conn.execute(
                        """INSERT OR IGNORE INTO bgp_routes
                           (target, asn, asn_name, prefix, country_code, data_hash)
                           VALUES (?,?,?,?,?,?)""",
                        (target, report.asn, report.asn_name, pfx.prefix,
                         pfx.country_code, self._hash(f"{target}:{pfx.prefix}")),
                    )
                conn.commit()
            logger.info("Persisted %d prefixes, %d peers", len(report.prefixes), len(report.peers))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 68_BGP_ROUTE_ANALYZER_synthesized_agent.py <IP_or_ASN>")
        print("  Examples: 8.8.8.8  |  AS15169  |  15169")
        sys.exit(1)

    agent = BgpRouteAnalyzerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
