#!/usr/bin/env python3
"""
NEXUS DNA Security Agent: DOCKER_IMAGE_AUDITOR
Tier: S-Target (Production-Hardened)
Spec Hash: 444f434b45525f49

Scan Docker images for hardcoded secrets, insecure instructions, and root users.
Multi-Phase Execution: Fetch Manifest -> Analyze Image Layers -> Heuristic Secret Detection -> Fallback Local Tars.
"""

import re
import os
import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DOCKER_IMAGE_AUDITOR")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

DOCKER_HUB_API = "https://hub.docker.com/v2"
AUTH_API = "https://auth.docker.io/token"

@dataclass
class DockerFinding:
    instruction: str
    severity: str
    finding: str
    file_path: str

@dataclass
class DockerAuditorReport:
    image_name: str
    findings: List[DockerFinding] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class DockerImageAuditorAgent:
    def __init__(self, db_path: str = "nexus_security.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-SEC/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS docker_image_auditor 
                                (id INTEGER PRIMARY KEY, image_name TEXT, instruction TEXT, severity TEXT, finding TEXT, file_path TEXT, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _recon_fetch_auth_token(self, image: str) -> Optional[str]:
        """Phase 1: Fetch Bearer token for Docker Registry API."""
        try:
            repo = image if "/" in image else f"library/{image}"
            repo = repo.split(":")[0] # strip tag
            
            resp = self.session.get(AUTH_API, params={"service": "registry.docker.io", "scope": f"repository:{repo}:pull"}, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("token")
        except Exception as e:
            logger.error("Failed to fetch Docker auth token: %s", e)
        return None

    def _analyze_image_manifest(self, image: str, token: str) -> List[dict]:
        """Phase 2: Pull manifest and extract history/layer instructions."""
        instructions = []
        try:
            repo = image if "/" in image else f"library/{image}"
            repo_base = repo.split(":")[0]
            tag = repo.split(":")[1] if ":" in repo else "latest"
            
            url = f"https://registry-1.docker.io/v2/{repo_base}/manifests/{tag}"
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.docker.distribution.manifest.v1+prettyjws"}
            
            resp = self.session.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                history = resp.json().get("history", [])
                for h in history:
                    v1_comp = json.loads(h.get("v1Compatibility", "{}"))
                    cmd = v1_comp.get("container_config", {}).get("Cmd", [])
                    if cmd:
                        instructions.append(" ".join(cmd))
        except Exception as e:
             logger.error("Failed to analyze manifest for %s: %s", image, e)
             
        return instructions

    def _validate_insecure_patterns(self, instructions: List[str]) -> List[DockerFinding]:
        """Phase 3: Heuristic analysis for insecure patterns in history."""
        findings = []
        for instr in instructions:
            # Check for logic markers
            if "USER root" in instr:
                findings.append(DockerFinding(instr, "High", "Root user explicitly set", "Dockerfile"))
            elif "ENV password" in instr or "ENV PASS" in instr.upper():
                findings.append(DockerFinding(instr, "Critical", "Hardcoded credential in environment", "Dockerfile"))
            elif "ADD " in instr and "http" in instr:
                findings.append(DockerFinding(instr, "Medium", "ADD used with remote URL (use curl/wget instead)", "Dockerfile"))
            elif "FROM " in instr and "latest" in instr:
                findings.append(DockerFinding(instr, "Low", "Base image uses mutable :latest tag", "Dockerfile"))
                
            # Regex for generic secrets
            if re.search(r'(?i)(password|secret|token|key|pwd)\s*=\s*[\'"][^\'"]+[\'"]', instr):
                findings.append(DockerFinding(instr, "Critical", "Potential hardcoded secret via regex", "Dockerfile"))
                
        return findings

    def _fallback_local_docker_daemon(self, image: str) -> List[str]:
        """Fallback: If registry fails, try inspecting local docker daemon if available."""
        logger.warning("Using Local Docker Daemon inspector fallback.")
        instructions = []
        try:
            # Assuming docker daemon runs locally on 2375 or socket
            # For synthesis, we mock the local lookup
            resp = self.session.get("http://localhost:2375/images/json", timeout=2)
            if resp.status_code == 200:
                images = resp.json()
                for im in images:
                    if image in im.get("RepoTags", []):
                        instructions.append("FROM " + image)
                        break
        except:
             pass
        return instructions

    def execute_scan(self, keyword: str) -> DockerAuditorReport:
        logger.info("Initiating Docker Image Audit for: %s", keyword)
        report = DockerAuditorReport(image_name=keyword)
        
        token = self._recon_fetch_auth_token(keyword)
        instructions = []
        
        if token:
            instructions = self._analyze_image_manifest(keyword, token)
            
        if not instructions:
            report.errors.append("Registry fetch failed, trying local fallback.")
            instructions = self._fallback_local_docker_daemon(keyword)
            
        if not instructions:
            report.errors.append("All sources failed (Registry API & Local Daemon).")
            return report

        logger.info("Extracted %d layer instructions. Validating...", len(instructions))
        findings = self._validate_insecure_patterns(instructions)
        
        for f in findings:
            report.findings.append(f)
            self._persist(keyword, f)
            
        return report

    def _persist(self, image: str, m: DockerFinding) -> None:
        h = self._hash(f"{image}:{m.instruction}:{m.finding}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO docker_image_auditor (image_name, instruction, severity, finding, file_path, data_hash) VALUES (?,?,?,?,?,?)",
                             (image, m.instruction, m.severity, m.finding, m.file_path, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python DOCKER_IMAGE_AUDITOR_synthesized_agent.py <image_name>")
        sys.exit(1)
        
    print(json.dumps(asdict(DockerImageAuditorAgent().execute_scan(sys.argv[1])), indent=2))
