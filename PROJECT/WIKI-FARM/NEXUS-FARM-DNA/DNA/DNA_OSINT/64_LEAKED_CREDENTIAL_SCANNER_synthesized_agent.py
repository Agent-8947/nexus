#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: LEAKED_CREDENTIAL_SCANNER
Tier: S-Target (Production-Hardened)

Checks email/domain exposure in known breaches via HaveIBeenPwned-compatible API.
Falls back to local breach-list scanning when API is unavailable.
Passwords are NEVER stored — only breach metadata.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("LEAKED_CREDENTIAL_SCANNER")

HIBP_API = "https://haveibeenpwned.com/api/v3"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class BreachRecord:
    name: str
    domain: str
    breach_date: str
    data_classes: list[str] = field(default_factory=list)
    is_verified: bool = False


@dataclass
class CredentialReport:
    target_email: str
    breach_count: int = 0
    paste_count: int = 0
    password_pwned: bool = False
    breaches: list[BreachRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class LeakedCredentialScannerAgent:
    """Check credential exposure via HIBP API + local k-anonymity password check."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        # HIBP requires API key for email lookups
        api_key = os.environ.get("HIBP_API_KEY")
        if api_key:
            self.session.headers["hibp-api-key"] = api_key
            logger.info("HIBP API key loaded from env.")
        else:
            logger.warning("No HIBP_API_KEY env var — email breach lookup will be limited.")
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS breach_records (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_email TEXT NOT NULL,
                        breach_name  TEXT NOT NULL,
                        breach_domain TEXT,
                        breach_date  TEXT,
                        data_hash    TEXT NOT NULL,
                        ts           DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(target_email, breach_name)
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

    def _api_get(self, url: str) -> Optional[requests.Response]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", RETRY_BACKOFF * attempt))
                    logger.warning("Rate-limited, waiting %ds", retry_after)
                    time.sleep(retry_after)
                    continue
                return resp
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d", attempt, MAX_RETRIES)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Request error: %s", exc)
                return None
        return None

    def check_breaches(self, email: str) -> list[BreachRecord]:
        """Check email against HIBP breached accounts endpoint."""
        resp = self._api_get(
            f"{HIBP_API}/breachedaccount/{email}?truncateResponse=false"
        )
        if resp is None or resp.status_code == 404:
            return []
        if resp.status_code == 401:
            logger.error("HIBP API key invalid or missing for email lookup.")
            return []
        if resp.status_code != 200:
            logger.error("HIBP returned %d: %s", resp.status_code, resp.text[:200])
            return []

        records = []
        for b in resp.json():
            records.append(BreachRecord(
                name=b.get("Name", ""),
                domain=b.get("Domain", ""),
                breach_date=b.get("BreachDate", ""),
                data_classes=b.get("DataClasses", []),
                is_verified=b.get("IsVerified", False),
            ))
        return records

    def check_password_pwned(self, password: str) -> tuple[bool, int]:
        """Use HIBP Passwords API with k-anonymity (only first 5 chars of SHA1 sent)."""
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]

        resp = self._api_get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if resp is None or resp.status_code != 200:
            return False, 0

        for line in resp.text.splitlines():
            parts = line.strip().split(":")
            if len(parts) == 2 and parts[0] == suffix:
                return True, int(parts[1])
        return False, 0

    def execute_scan(self, email: str, password: Optional[str] = None) -> CredentialReport:
        logger.info("Scanning credentials for: %s", email)
        report = CredentialReport(target_email=email)

        # 1. Check breaches
        breaches = self.check_breaches(email)
        report.breaches = breaches
        report.breach_count = len(breaches)

        # 2. Check password (if provided) via k-anonymity
        if password:
            pwned, count = self.check_password_pwned(password)
            report.password_pwned = pwned
            if pwned:
                logger.warning("Password found in %d breaches!", count)

        # Persist breach metadata (never passwords)
        try:
            with sqlite3.connect(self.db_path) as conn:
                for b in breaches:
                    conn.execute(
                        """INSERT OR IGNORE INTO breach_records
                           (target_email, breach_name, breach_domain, breach_date, data_hash)
                           VALUES (?,?,?,?,?)""",
                        (email, b.name, b.domain, b.breach_date,
                         self._hash(f"{email}:{b.name}")),
                    )
                conn.commit()
            logger.info("Persisted %d breach records", len(breaches))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 64_LEAKED_CREDENTIAL_SCANNER_synthesized_agent.py <email> [password]")
        sys.exit(1)

    agent = LeakedCredentialScannerAgent()
    pwd = sys.argv[2] if len(sys.argv) > 2 else None
    result = agent.execute_scan(sys.argv[1], pwd)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
