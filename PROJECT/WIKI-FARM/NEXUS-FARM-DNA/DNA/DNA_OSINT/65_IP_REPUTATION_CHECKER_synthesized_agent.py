#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: IP_REPUTATION_CHECKER
Tier: S-Target (Production-Hardened)

Checks IP reputation via multiple free public APIs:
  - ip-api.com (geolocation + ISP + proxy detection)
  - ipinfo.io  (ASN + org)

No API keys required for basic tier.
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
logger = logging.getLogger("IP_REPUTATION_CHECKER")

MAX_RETRIES = 3
RETRY_BACKOFF = 1.5


@dataclass
class IpReputation:
    ip: str
    country: str = ""
    city: str = ""
    isp: str = ""
    org: str = ""
    asn: str = ""
    is_proxy: bool = False
    is_hosting: bool = False
    is_mobile: bool = False
    reverse_dns: str = ""
    threat_score: float = 0.0  # 0.0 = clean, 1.0 = malicious


@dataclass
class IpReputationReport:
    targets: list[IpReputation] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class IpReputationCheckerAgent:
    """Multi-source IP reputation enrichment."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS ip_reputation (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip           TEXT NOT NULL,
                        country      TEXT,
                        city         TEXT,
                        isp          TEXT,
                        org          TEXT,
                        asn          TEXT,
                        is_proxy     INTEGER DEFAULT 0,
                        is_hosting   INTEGER DEFAULT 0,
                        threat_score REAL DEFAULT 0.0,
                        data_hash    TEXT NOT NULL,
                        ts           DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(ip, data_hash)
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

    def _api_get(self, url: str, timeout: int = 10) -> Optional[dict]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=timeout)
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d for %s", attempt, MAX_RETRIES, url)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Request error: %s", exc)
                return None
        return None

    def _enrich_ip_api(self, ip: str) -> dict:
        """Enrich via ip-api.com (free, 45 req/min)."""
        data = self._api_get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,as,proxy,hosting,mobile,reverse"
        )
        if data and data.get("status") == "success":
            return data
        return {}

    def _enrich_ipinfo(self, ip: str) -> dict:
        """Enrich via ipinfo.io (free tier, 50k/month)."""
        data = self._api_get(f"https://ipinfo.io/{ip}/json")
        return data or {}

    def _calculate_threat_score(self, info: dict) -> float:
        """Heuristic threat scoring based on enrichment data."""
        score = 0.0
        if info.get("proxy"):
            score += 0.4
        if info.get("hosting"):
            score += 0.2
        # Known high-risk ISP patterns
        isp_lower = info.get("isp", "").lower()
        risk_isps = ["tor", "vpn", "proxy", "hosting", "cloud", "dedicated"]
        if any(r in isp_lower for r in risk_isps):
            score += 0.2
        return min(score, 1.0)

    def check_ip(self, ip: str) -> IpReputation:
        """Full enrichment of a single IP from multiple sources."""
        logger.info("Checking reputation for IP: %s", ip)

        # Source 1: ip-api.com
        ip_api_data = self._enrich_ip_api(ip)
        time.sleep(0.1)  # rate-limit compliance

        # Source 2: ipinfo.io
        ipinfo_data = self._enrich_ipinfo(ip)

        # Merge
        rep = IpReputation(
            ip=ip,
            country=ip_api_data.get("country", ipinfo_data.get("country", "")),
            city=ip_api_data.get("city", ipinfo_data.get("city", "")),
            isp=ip_api_data.get("isp", ""),
            org=ip_api_data.get("org", ipinfo_data.get("org", "")),
            asn=ip_api_data.get("as", ipinfo_data.get("org", "")),
            is_proxy=ip_api_data.get("proxy", False),
            is_hosting=ip_api_data.get("hosting", False),
            is_mobile=ip_api_data.get("mobile", False),
            reverse_dns=ip_api_data.get("reverse", ""),
        )
        rep.threat_score = self._calculate_threat_score(ip_api_data)
        return rep

    def execute_scan(self, *ips: str) -> IpReputationReport:
        report = IpReputationReport()

        for ip in ips:
            try:
                rep = self.check_ip(ip)
                report.targets.append(rep)
            except Exception as exc:
                logger.error("Failed to check %s: %s", ip, exc)
                report.errors.append(f"{ip}: {exc}")

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rep in report.targets:
                    snapshot = json.dumps(asdict(rep), sort_keys=True)
                    conn.execute(
                        """INSERT OR IGNORE INTO ip_reputation
                           (ip, country, city, isp, org, asn, is_proxy, is_hosting, threat_score, data_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (rep.ip, rep.country, rep.city, rep.isp, rep.org, rep.asn,
                         int(rep.is_proxy), int(rep.is_hosting), rep.threat_score,
                         self._hash(snapshot)),
                    )
                conn.commit()
            logger.info("Persisted %d IP reputation records", len(report.targets))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 65_IP_REPUTATION_CHECKER_synthesized_agent.py <ip1> [ip2] ...")
        sys.exit(1)

    agent = IpReputationCheckerAgent()
    result = agent.execute_scan(*sys.argv[1:])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
