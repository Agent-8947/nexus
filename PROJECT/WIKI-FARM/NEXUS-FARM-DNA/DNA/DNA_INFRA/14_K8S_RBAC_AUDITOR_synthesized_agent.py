#!/usr/bin/env python3
"""
NEXUS DNA Infra Agent: K8S_RBAC_AUDITOR
Tier: A-Target (Production-Hardened)
Spec Hash: 4b38735f52424143

Audit Kubernetes RBAC for overly permissive rules (e.g. cluster-admin).
"""

import json
import logging
import requests
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("K8S_RBAC_AUDITOR")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class RbacFinding:
    subject: str
    role: str
    is_dangerous: int

@dataclass
class K8sRbacReport:
    cluster_api_url: str
    findings: List[RbacFinding] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class K8sRbacAuditorAgent:
    def __init__(self, db_path: str = "nexus_infra.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-INFRA/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS k8s_rbac_auditor 
                                (id INTEGER PRIMARY KEY, cluster_url TEXT, subject TEXT, role TEXT, is_dangerous INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_audit(self, cluster_api_url: str, token: Optional[str] = None) -> K8sRbacReport:
        logger.info("Auditing RBAC for cluster: %s", cluster_api_url)
        report = K8sRbacReport(cluster_api_url=cluster_api_url)
        
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            
        url = f"{cluster_api_url}/apis/rbac.authorization.k8s.io/v1/clusterrolebindings"
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=15, verify=False)
                resp.raise_for_status()
                
                bindings = resp.json().get("items", [])
                for b in bindings:
                    role_ref = b.get("roleRef", {})
                    if role_ref.get("name") == "cluster-admin":
                        finding = RbacFinding(
                            subject=b.get("subjects", [{}])[0].get("name", "unknown"),
                            role="cluster-admin",
                            is_dangerous=1
                        )
                        report.findings.append(finding)
                        self._persist(cluster_api_url, finding)
                break
            except Exception as e:
                logger.error("Audit failed on attempt %d: %s", attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(f"API unreachable: {e}")
                    
        return report

    def _persist(self, url: str, m: RbacFinding) -> None:
        h = self._hash(f"{url}:{m.subject}:{m.role}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO k8s_rbac_auditor (cluster_url, subject, role, is_dangerous, data_hash) VALUES (?,?,?,?,?)",
                             (url, m.subject, m.role, m.is_dangerous, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 14_K8S_RBAC_AUDITOR_synthesized_agent.py <cluster_url> [token]")
        sys.exit(1)
    token = sys.argv[2] if len(sys.argv) > 2 else None
    print(json.dumps(asdict(K8sRbacAuditorAgent().execute_audit(sys.argv[1], token)), indent=2))
