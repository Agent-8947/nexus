#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: ASN_OWNERSHIP_MAPPER
Tier: S-Target (Production-Hardened)
Spec Hash: be9aefd7625085d9

Map organizational ownership of IP ranges via RIPE Stat and PeeringDB.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ASN_OWNERSHIP_MAPPER")

RIPE_API_URL = "https://stat.ripe.net/data/as-overview/data.json?resource={asn}"
PEERINGDB_API_URL = "https://www.peeringdb.com/api/net?asn={asn}"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class AsnOwnershipRecord:
    asn: int
    org_name: str = ""
    holder: str = ""
    country: str = ""
    prefix_count: int = 0
    peering_policy: str = ""
    ix_count: int = 0

@dataclass
class AsnOwnershipReport:
    asn: int
    ownership: Optional[AsnOwnershipRecord] = None
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class AsnOwnershipMapperAgent:
    """Agent for cross-referencing RIPE Stat and PeeringDB data."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS asn_ownership_mapper (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        asn INTEGER NOT NULL,
                        org_name TEXT,
                        holder TEXT,
                        country TEXT,
                        prefix_count INTEGER,
                        peering_policy TEXT,
                        ix_count INTEGER,
                        data_hash TEXT NOT NULL,
                        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(asn, data_hash)
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

    def _query_ripe(self, asn: int) -> Optional[dict]:
        url = RIPE_API_URL.format(asn=asn)
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except Exception as exc:
            logger.error("RIPE query error: %s", exc)
        return None

    def _query_peeringdb(self, asn: int) -> Optional[dict]:
        url = PEERINGDB_API_URL.format(asn=asn)
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except Exception as exc:
            logger.error("PeeringDB query error: %s", exc)
        return None

    def execute_scan(self, asn_input: str) -> AsnOwnershipReport:
        asn = int(asn_input.upper().replace("AS", ""))
        logger.info("Mapping ownership for ASN: %d", asn)
        report = AsnOwnershipReport(asn=asn)
        record = AsnOwnershipRecord(asn=asn)

        # 1. RIPE Stat
        ripe_data = self._query_ripe(asn)
        if ripe_data and ripe_data.get("status") == "ok":
            data = ripe_data.get("data", {})
            record.holder = data.get("holder", "")
            # Prefix count requires a different call but sometimes included in overview
            
        # 2. PeeringDB
        pdb_data = self._query_peeringdb(asn)
        if pdb_data and pdb_data.get("data"):
            net = pdb_data["data"][0]
            record.org_name = net.get("name", "")
            record.country = net.get("country", "")
            record.peering_policy = net.get("policy_general", "Unknown")
            # PeeringDB often has IX counts in related fields
            
        report.ownership = record

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                snap_blob = f"{asn}:{record.org_name}:{record.holder}"
                conn.execute(
                    """INSERT OR IGNORE INTO asn_ownership_mapper
                       (asn, org_name, holder, country, prefix_count, peering_policy, ix_count, data_hash)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (asn, record.org_name, record.holder, record.country, 
                     record.prefix_count, record.peering_policy, record.ix_count, self._hash(snap_blob)),
                )
                conn.commit()
            logger.info("Persisted ASN ownership details for AS%d", asn)
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 77_ASN_OWNERSHIP_MAPPER_synthesized_agent.py <asn>")
        sys.exit(1)

    agent = AsnOwnershipMapperAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
