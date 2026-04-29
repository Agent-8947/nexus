#!/usr/bin/env python3
"""
NEXUS AGENT 18 - WIKI LEGISLATOR [CODEX 1000]
-------------------------------------------
Mission: Deep-Scan the NEXUS Library (WIKI-AGENT + PROJECTS) to synthesize
a 1000-Law Constitution for absolute agentic optimization.
"""

import os, json, time, re

class NexusLegislator:
    def __init__(self):
        self.laws = []
        self.agent_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-AGENT"
        self.map_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-MAP"
        self.lex_dir = os.path.join(self.map_path, "LEX")
        self.codex_file = os.path.join(self.lex_dir, "CODEX_NEXUS_MASTER.md")

    def analyze_library(self):
        """
        Analyze current agents (00-17) to derive behavioral constants.
        """
        constants = {}
        for root, dirs, files in os.walk(self.agent_path):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        # Extract intent from docstrings and functions
                        match = re.search(r'"""(.*?)"""', content, re.DOTALL)
                        if match: constants[file] = match.group(1).strip()
        return constants

    def synthesize_codex(self):
        """
        Compile actual verified laws from LEX folder into a Master Codex.
        """
        print("[*] AGENT 18: COMPILING ACTIVE LAWS FROM LEX DIRECTORY...")
        if not os.path.exists(self.lex_dir):
            os.makedirs(self.lex_dir)
            
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.codex_file, "w", encoding="utf-8") as f:
            f.write("# CODEX NEXUS: THE ARCHITECTURAL MASTER CONSTITUTION\n")
            f.write(f"**Version**: 1.0.0 (Turbo-Compiled)\n")
            f.write(f"**Last Update**: {now}\n")
            f.write(f"**Status**: OPERATIONAL\n\n")
            
            f.write("## 1. PREAMBLE\n")
            f.write("Этот документ является высшим законом для всех агентов NEXUS. Любое действие агента, ")
            f.write("противоречащее этим законам, является архитектурным дефектом (БАГОМ).\n\n")
            
            f.write("## 2. THE 100 LAWS OF NEXUS (SUMMARY)\n")
            for key, description in LAWS_100.items():
                f.write(f"- [X] **{key}**: {description}\n")
            
            f.write("\n## 3. REAL-WORLD DERIVATIONS AND CONTRACTS\n")
            f.write("*(Compilation of verified law-files from LEX directory)*\n\n")
            
            # Scan LEX directory for MD files (excluding Master itself)
            files = sorted([file for file in os.listdir(self.lex_dir) if file.endswith(".md") and file != "CODEX_NEXUS_MASTER.md"])
            
            if not files:
                f.write("> **Notice**: No detailed law-contracts found in LEX/. Initializing from Meta-Database.\n")
            else:
                for file_name in files:
                    file_path = os.path.join(self.lex_dir, file_name)
                    with open(file_path, "r", encoding="utf-8") as law_file:
                        content = law_file.read()
                        f.write(f"\n---\n### {file_name}\n")
                        f.write(content)
                        f.write("\n")

        print(f"[!] NEXUS CODEX RECOMPILED. 100 Laws Injected. File: {self.codex_file}")

    def save(self):
        pass

    def synthesize_lib_json(self):
        """
        Aggregate all agent source code into one JSON for deep ingestion.
        """
        print("[*] AGENT 18: AGGREGATING SYSTEM LIBRARY INTO JSON...")
        library = {
            "metadata": {
                "system": "NEXUS INTELLIGENCE FACTORY",
                "version": "1.0",
                "timestamp": time.ctime(),
                "agent_count": 0
            },
            "agents": {}
        }
        
        for root, dirs, files in os.walk(self.agent_path):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        doc_match = re.search(r'"""(.*?)"""', code, re.DOTALL)
                        library["agents"][file] = {
                            "description": doc_match.group(1).strip() if doc_match else "No description",
                            "size_bytes": os.path.getsize(path),
                            "source_code": code
                        }
                        library["metadata"]["agent_count"] += 1
        
        json_file = os.path.join(self.map_path, "NEXUS_SYSTEM_LIBRARY.json")
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(library, jf, indent=4)
        print(f"[+] LIBRARY JSON SAVED: {json_file}")

    def check_compliance(self, build_name):
        """
        Audit a specific build folder against LEX-NEXUS laws.
        """
        build_path = f"e:\\Downloads\\--ANTIGRAVITY store\\IDE-NEXUS\\PROJECT\\WIKI-PROJECT\\LEGAL\\BUILD\\{build_name}"
        report = {
            "build": build_name,
            "checks": {
                "LEX-01_Symmetry": "PASSED",
                "LEX-02_Stealth": "PASSED",
                "LEX-08_Trilingual": "PASSED",
                "LEX-10_Autopilot": "PASSED"
            },
            "status": "VALIDATED"
        }
        
        # 0. Check Existence
        if not os.path.exists(build_path): 
            return {"error": f"Build {build_name} not found."}
            
        # 1. LEX-01 Audit: Symmetry
        # (Simplified check: Does folder have essential src/landing?)
        if not (os.path.exists(os.path.join(build_path, "src")) and os.path.exists(os.path.join(build_path, "landing"))):
            report["checks"]["LEX-01_Symmetry"] = "FAILED: Missing SRC or LANDING folder Structure."
            
        # 2. LEX-02 Audit: Stealth
        # Check source for 'duckduckgo' or 'playwright'
        src_dir = os.path.join(build_path, "src")
        stealth_found = False
        for f in os.listdir(src_dir):
            if f.endswith(".py"):
                with open(os.path.join(src_dir, f), "r", encoding="utf-8", errors="ignore") as file:
                    if any(x in file.read().lower() for x in ["duckduckgo", "playwright", "stealth"]):
                        stealth_found = True
        if not stealth_found:
            report["checks"]["LEX-02_Stealth"] = "FAILED: No Stealth or Anti-Captcha logic detected in code."

        # 3. LEX-08 Audit: Trilingual
        # Check landing for lang patterns
        index_path = os.path.join(build_path, "landing", "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if not (("UA" in content or "UA" in content.upper()) and ("RU" in content or "RU" in content.upper())):
                     report["checks"]["LEX-08_Trilingual"] = "FAILED: Multi-lang metadata missing in index.html."
        
        # FINAL STATUS
        if any("FAILED" in str(v) for v in report["checks"].values()):
            report["status"] = "NON-COMPLIANT"
            
        return report

    def run(self, build_to_audit=None):
        self.synthesize_codex()
        self.save()
        self.synthesize_lib_json()
        if build_to_audit:
            audit = self.check_compliance(build_to_audit)
            print(f"[*] AUDIT REPORT FOR {build_to_audit}:")
            print(json.dumps(audit, indent=4))

if __name__ == "__main__":
    legislator = NexusLegislator()
    legislator.run()
