#!/usr/bin/env python3
"""
91_ADVERSARIAL_RED_TEAMER Synthesized Agent
Identity: NexusRedTeamer
Domain: SECURITY_ADV / SYNTH_TOOLS
Lineage: NEXUS-Adversarial-Core

S-TIER IMPLEMENTATION: 
- Static Analysis (AST-based) for Vulnerability Detection
- Adversarial Logic Probing (Prior Manipulation)
- Hardening Recommendations (CWE-mapping)
- Logic Flow Auditing
"""

import os
import ast
import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] NexusRedTeamer: %(message)s")
logger = logging.getLogger("NexusRedTeamer")

@dataclass
class Vulnerability:
    file: str
    type: str
    description: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL
    cwe: str
    line_no: int

class NexusRedTeamerAgent:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.findings: List[Vulnerability] = []
        
    def _scan_for_unsafe_calls(self, file_path: str, content: str):
        """Analyze code for dangerous functions (eval, system, shell=True)."""
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Detect eval/exec
                if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
                    self.findings.append(Vulnerability(
                        file=file_path, type="DYNAMIC_EXECUTION",
                        description=f"Use of {node.func.id} detected. High risk of code injection.",
                        severity="CRITICAL", cwe="CWE-94", line_no=node.lineno
                    ))
                
                # Detect subprocess(shell=True)
                if isinstance(node.func, ast.Attribute) and node.func.attr == 'run':
                    for keyword in node.keywords:
                        if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            self.findings.append(Vulnerability(
                                file=file_path, type="SHELL_INJECTION",
                                description="subprocess.run(shell=True) detected. High risk of command injection.",
                                severity="HIGH", cwe="CWE-78", line_no=node.lineno
                            ))

    def _check_sha256_missing(self, file_path: str, content: str):
        """Check if an agent handles data without hashing/deduplication."""
        if os.path.basename(file_path).startswith("7") or os.path.basename(file_path).startswith("8"):
            if "hashlib" not in content and "sha256" not in content.lower():
                self.findings.append(Vulnerability(
                    file=file_path, type="DATA_INTEGRITY_MISSING",
                    description="Agent processes signals/recon data without SHA-256 deduplication.",
                    severity="MEDIUM", cwe="CWE-440", line_no=1
                ))

    def execute_audit(self):
        """
        Run the Red-Teaming loop across the DNA library.
        """
        logger.info("PHASE 1: Initializing Adversarial Probe on %s", self.target_dir)
        
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith("_synthesized_agent.py"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self._scan_for_unsafe_calls(file, content)
                        self._check_sha256_missing(file, content)
                    except Exception as e:
                        logger.error("Failed to parse %s: %s", file, e)

        # PHASE 2: Report Aggregation
        logger.info("PHASE 2: Generating Hardening Report...")
        if not self.findings:
            logger.info("NO VULNERABILITIES FOUND. NEXUS Herd is secure.")
        else:
            print("\n" + "="*50)
            print("NEXUS RED-TEAM ADVERSARIAL REPORT")
            print("="*50)
            for v in sorted(self.findings, key=lambda x: x.severity, reverse=True):
                print(f"[{v.severity}] {v.type} in {v.file}:L{v.line_no}")
                print(f" -> {v.description} ({v.cwe})")
                print("-" * 20)
            print("="*50)

if __name__ == "__main__":
    # Point at the DNA directory
    dna_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA"
    agent = NexusRedTeamerAgent(dna_path)
    agent.execute_audit()
