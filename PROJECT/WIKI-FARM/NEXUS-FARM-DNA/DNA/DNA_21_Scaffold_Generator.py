#!/usr/bin/env python3
"""
NEXUS SCAFFOLD GENERATOR v3.0 [HARDENED FOR WEAK MODELS]
==========================================================
Strategy: 90% of code is pre-written. LLM fills only small focused blocks.
Even a 3B parameter model produces 100% quality output.

Coverage: ALL 8 NEXUS roles (collector, processor, analyzer, orchestrator,
          storage, presentation, library, payload).
"""

import json
from pathlib import Path
from datetime import datetime

DNA_DIR = Path(__file__).resolve().parent

# ═══════════════════════════════════════════════════════════════════════════
# ROLE SCAFFOLDS — each is 90%+ complete, LLM fills only marked [FILL] blocks
# ═══════════════════════════════════════════════════════════════════════════

SCAFFOLD_COLLECTOR = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: collector | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")

# ── Collection Patterns ──────────────────────────────────────────────────
# [FILL:PATTERNS] Define 3-5 regex patterns leveraging Domains: {domains}
# Example: PATTERNS = {{"api_key": r"(?i)(api[_-]?key|token)\\s*[:=]\\s*[\\w]{{16,}}"}}
PATTERNS = {{
    "sensitive_file": r"(?i)(password|secret|token|credential|apikey)",
    "config_exposure": r"(?i)(database_url|db_pass|aws_secret)",
    "hardcoded_ip": r"\\b(?:(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.?){{4}}\\b",
}}
# ─────────────────────────────────────────────────────────────────────────

# [FILL:EXTENSIONS] File extensions to scan based on Domains: {domains}
TARGET_EXTENSIONS = {{".py", ".js", ".json", ".yaml", ".yml", ".toml", ".env", ".cfg", ".ini", ".conf"}}


class DataCollector:
    """Scans targets and extracts findings matching predefined patterns."""

    def __init__(self):
        self.stats = {{"items_collected": 0, "files_scanned": 0, "errors": 0}}

    def collect(self, target: Path) -> list[dict]:
        """Scan target directory for pattern matches."""
        findings = []

        if not target.exists():
            logger.error(f"Target not found: {{target}}")
            return findings

        for fpath in target.rglob("*"):
            if not fpath.is_file():
                continue
            if fpath.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            if ".git" in fpath.parts or "__pycache__" in fpath.parts:
                continue

            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                self.stats["files_scanned"] += 1

                for rule_name, pattern in PATTERNS.items():
                    for match in re.finditer(pattern, content):
                        line_num = content[:match.start()].count("\\n") + 1
                        findings.append({{
                            "type": rule_name,
                            "content": match.group(0)[:200],
                            "file": str(fpath.relative_to(target)),
                            "line": line_num,
                            "severity": "HIGH" if "secret" in rule_name.lower() or "password" in rule_name.lower() else "MEDIUM",
                        }})
                        self.stats["items_collected"] += 1

            except Exception as e:
                self.stats["errors"] += 1
                logger.debug(f"Skip {{fpath.name}}: {{e}}")

        logger.info(f"[SCAN] {{self.stats['files_scanned']}} files, {{self.stats['items_collected']}} findings")
        return findings


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--target", required=True, help="Directory to scan")
    parser.add_argument("--output", default="collection_report.json", help="Output JSON")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    collector = DataCollector()
    findings = collector.collect(target)

    report = {{
        "agent": "{agent_name}",
        "version": "1.0-gen{generation}",
        "timestamp": datetime.now().isoformat(),
        "target": str(target),
        "stats": collector.stats,
        "findings": findings
    }}

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] {{len(findings)}} findings -> {{output}}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_ANALYZER = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: analyzer | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")

# ── Scoring Weights ──────────────────────────────────────────────────────
# [FILL:WEIGHTS] Adjust severity weights for your domain.
SEVERITY_SCORES = {{"CRITICAL": 1.0, "HIGH": 0.75, "MEDIUM": 0.45, "LOW": 0.15, "INFO": 0.05}}

# [FILL:RULES] Map finding types to priority classifications.
PRIORITY_RULES = {{
    "sensitive_file": "P0-IMMEDIATE",
    "config_exposure": "P1-URGENT",
    "hardcoded_ip": "P2-REVIEW",
}}
# ─────────────────────────────────────────────────────────────────────────


class DataAnalyzer:
    """Scores and prioritizes findings from a collector report."""

    def __init__(self):
        self.stats = {{"total": 0, "by_priority": {{}}}}

    def analyze(self, findings: list[dict]) -> list[dict]:
        """Score each finding and assign priority."""
        enriched = []
        for f in findings:
            severity = f.get("severity", "MEDIUM")
            risk_score = SEVERITY_SCORES.get(severity, 0.3)
            finding_type = f.get("type", "unknown")
            priority = PRIORITY_RULES.get(finding_type, "P2-REVIEW")

            # [FILL:REMEDIATION] Add domain-specific remediation advice.
            remediation_map = {{
                "sensitive_file": "Rotate credentials. Move to vault (HashiCorp/AWS SSM).",
                "config_exposure": "Use environment variables. Never commit .env files.",
                "hardcoded_ip": "Use DNS or config-driven service discovery.",
            }}

            f["risk_score"] = round(risk_score, 3)
            f["priority"] = priority
            f["remediation"] = remediation_map.get(finding_type, "Review and assess manually.")
            f["rule_id"] = finding_type.upper()
            enriched.append(f)

            self.stats["total"] += 1
            self.stats["by_priority"][priority] = self.stats["by_priority"].get(priority, 0) + 1

        enriched.sort(key=lambda x: x["risk_score"], reverse=True)
        return enriched


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--input", required=True, help="Collector JSON report")
    parser.add_argument("--output", default="analysis_report.json", help="Output JSON")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {{input_path}}")
        sys.exit(1)

    report = json.loads(input_path.read_text(encoding="utf-8"))
    findings = report.get("findings", [])
    logger.info(f"[*] Analyzing {{len(findings)}} findings...")

    analyzer = DataAnalyzer()
    enriched = analyzer.analyze(findings)

    scores = [f["risk_score"] for f in enriched]
    result = {{
        "agent": "{agent_name}",
        "version": "1.0-gen{generation}",
        "timestamp": datetime.now().isoformat(),
        "source_agent": report.get("agent", "unknown"),
        "analysis": {{
            "total_findings": len(enriched),
            "top_risk_score": max(scores) if scores else 0,
            "mean_risk_score": round(sum(scores) / len(scores), 3) if scores else 0,
            "risk_verdict": "CRITICAL" if any(s >= 0.75 for s in scores) else "ELEVATED" if any(s >= 0.45 for s in scores) else "LOW",
            "by_priority": analyzer.stats["by_priority"],
        }},
        "enriched_findings": enriched
    }}

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Analysis -> {{output}}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_ORCHESTRATOR = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: orchestrator | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import json
import time
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")

AGENT_DIR = Path(__file__).resolve().parent


def run_agent(script: Path, args: list, label: str) -> bool:
    """Execute a child agent as subprocess."""
    if not script.exists():
        logger.error(f"[{{label}}] Agent not found: {{script}}")
        return False
    cmd = [sys.executable, str(script)] + args
    logger.info(f"[{{label}}] Running: {{script.name}}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            logger.info(f"[{{label}}] OK")
            if result.stdout.strip():
                print(result.stdout)
            return True
        else:
            logger.error(f"[{{label}}] Failed (exit {{result.returncode}})")
            if result.stderr:
                for line in result.stderr.strip().split("\\n")[-3:]:
                    logger.error(f"  {{line}}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"[{{label}}] Timeout 120s")
        return False
    except Exception as e:
        logger.error(f"[{{label}}] Error: {{e}}")
        return False


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument("--workdir", default="output", help="Output directory")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    t0 = time.monotonic()
    logger.info("=== Pipeline Start ===")

    # [FILL:PIPELINE] Define pipeline stages.
    # Example:
    # ok1 = run_agent(AGENT_DIR / "collector.py",
    #   ["--target", str(target), "--output", str(workdir / "step1.json")], "COLLECT")
    # ok2 = run_agent(AGENT_DIR / "analyzer.py",
    #   ["--input", str(workdir / "step1.json"), "--output", str(workdir / "step2.json")], "ANALYZE")

    elapsed = round(time.monotonic() - t0, 1)
    logger.info(f"[DONE] Pipeline complete in {{elapsed}}s")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_PROCESSOR = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: processor | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")


class DataProcessor:
    """Transforms and normalizes raw data into structured format."""

    def __init__(self):
        self.stats = {{"processed": 0, "skipped": 0, "errors": 0}}

    def process(self, records: list[dict]) -> list[dict]:
        """Transform each record into normalized form."""
        results = []
        for rec in records:
            try:
                # [FILL:TRANSFORM] Normalize fields. Examples:
                # - Lowercase all string fields
                # - Parse dates into ISO format
                # - Extract domain from URLs
                normalized = {{
                    "id": rec.get("id", self.stats["processed"]),
                    "source": str(rec.get("source", "unknown")).lower().strip(),
                    "content": str(rec.get("content", ""))[:500],
                    "timestamp": rec.get("timestamp", datetime.now().isoformat()),
                    "tags": [t.lower().strip() for t in rec.get("tags", [])],
                }}
                results.append(normalized)
                self.stats["processed"] += 1
            except Exception as e:
                self.stats["errors"] += 1
                logger.debug(f"Skip record: {{e}}")
        return results


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--input", required=True, help="Input JSON")
    parser.add_argument("--output", default="processed.json", help="Output JSON")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Not found: {{input_path}}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    records = data if isinstance(data, list) else data.get("records", data.get("findings", []))

    processor = DataProcessor()
    results = processor.process(records)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({{"agent": "{agent_name}", "stats": processor.stats, "records": results}}, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] {{processor.stats['processed']}} records -> {{output}}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_STORAGE = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: storage | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import json
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")


class PersistentStore:
    """SQLite-backed persistent storage for NEXUS agent data."""

    def __init__(self, db_path: str = "nexus_store.db"):
        self.db_path = db_path
        self.stats = {{"inserted": 0, "queried": 0}}
        self._init()

    def _init(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT, category TEXT, data TEXT, ts TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON records(source)")

    def insert(self, source: str, category: str, data: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO records (source, category, data, ts) VALUES (?,?,?,?)",
                         (source, category, json.dumps(data), datetime.now().isoformat()))
        self.stats["inserted"] += 1

    def query(self, source: str = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if source:
                rows = conn.execute("SELECT * FROM records WHERE source=? ORDER BY ts DESC LIMIT ?", (source, limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM records ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
        self.stats["queried"] += 1
        return [dict(r) for r in rows]

    def export_json(self, path: Path):
        records = self.query(limit=10000)
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"[EXPORT] {{len(records)}} records -> {{path}}")


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--ingest", help="JSON file to ingest")
    parser.add_argument("--query", help="Query by source name")
    parser.add_argument("--export", help="Export DB to JSON")
    parser.add_argument("--db", default="nexus_store.db", help="DB path")
    args = parser.parse_args()

    store = PersistentStore(args.db)
    if args.ingest:
        data = json.loads(Path(args.ingest).read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("findings", data.get("records", []))
        for item in items:
            store.insert(item.get("source", "unknown"), item.get("type", "misc"), item)
        logger.info(f"[DONE] Ingested {{store.stats['inserted']}} records")
    elif args.query:
        results = store.query(args.query)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.export:
        store.export_json(Path(args.export))
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_PRESENTATION = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: presentation | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")


class ReportGenerator:
    """Generates human-readable Markdown reports from analysis data."""

    def generate(self, data: dict, title: str = "NEXUS Report") -> str:
        lines = [
            f"# {{title}}",
            f"",
            f"**Generated:** {{datetime.now().isoformat()}}",
            f"**Agent:** {agent_name}",
            f"",
            f"## Summary",
            f"",
        ]

        analysis = data.get("analysis", {{}})
        for key, val in analysis.items():
            if isinstance(val, dict):
                lines.append(f"### {{key}}")
                for k, v in val.items():
                    lines.append(f"- **{{k}}**: {{v}}")
            else:
                lines.append(f"- **{{key}}**: {{val}}")

        findings = data.get("enriched_findings", data.get("findings", []))
        if findings:
            lines.extend(["", "## Top Findings", "",
                          "| # | Risk | Type | Source | Detail |",
                          "|---|---|---|---|---|"])
            for i, f in enumerate(findings[:15], 1):
                lines.append(f"| {{i}} | {{f.get('risk_score', '?')}} | {{f.get('type', '?')}} | {{f.get('file', '?')}} | {{str(f.get('content', ''))[:60]}} |")

        lines.extend(["", "---", f"*Auto-generated by NEXUS Pipeline*"])
        return "\\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--input", required=True, help="Analysis JSON")
    parser.add_argument("--output", default="report.md", help="Output Markdown")
    parser.add_argument("--title", default="NEXUS Intelligence Report", help="Report title")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    gen = ReportGenerator()
    md = gen.generate(data, title=args.title)

    Path(args.output).write_text(md, encoding="utf-8")
    logger.info(f"[DONE] Report -> {{args.output}}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_LIBRARY = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: library | Security: {security} | Interface: {interface} | Domains: {domains}
"""

import sys
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")


# ── Reusable Utilities ───────────────────────────────────────────────────

def normalize_text(text: str) -> str:
    """Strip, lowercase, collapse whitespace."""
    return re.sub(r"\\s+", " ", text.strip().lower())

def extract_json_block(text: str) -> dict | None:
    """Extract first JSON object from text."""
    start = text.find("{{")
    end = text.rfind("}}") + 1
    if start == -1 or end == 0:
        return None
    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None

def chunk_list(lst: list, size: int) -> list[list]:
    """Split list into chunks of given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]

def safe_read(path: Path, encoding: str = "utf-8") -> str:
    """Read file with error handling."""
    try:
        return path.read_text(encoding=encoding, errors="ignore")
    except Exception as e:
        logger.error(f"Read failed: {{path}} — {{e}}")
        return ""

# [FILL:UTILS] Add domain-specific utility functions.


def main():
    parser = argparse.ArgumentParser(description="{agent_name} — utility library")
    parser.add_argument("--test", action="store_true", help="Run self-test")
    args = parser.parse_args()

    if args.test:
        assert normalize_text("  Hello   World  ") == "hello world"
        assert chunk_list([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]
        assert extract_json_block('blah {{"a":1}} blah') == {{"a": 1}}
        logger.info("[TEST] All self-tests passed.")
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

SCAFFOLD_PAYLOAD = '''#!/usr/bin/env python3
"""
{agent_name} [NEXUS SYNTHESIZED Gen-{generation}]
Mission: {mission}
Heritage: {parent_a} + {parent_b}
Role: payload | Security: {security} | Interface: {interface} | Domains: {domains}

WARNING: This agent performs active operations. Use responsibly.
"""

import sys
import json
import hashlib
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{agent_name}")


class PayloadEngine:
    """Generates and validates operational payloads."""

    def __init__(self):
        self.stats = {{"generated": 0, "validated": 0}}

    def generate(self, config: dict) -> dict:
        """Create a payload from configuration."""
        payload_data = json.dumps(config, sort_keys=True)
        checksum = hashlib.sha256(payload_data.encode()).hexdigest()[:16]

        payload = {{
            "id": f"PL-{{checksum}}",
            "config": config,
            "checksum": checksum,
            "generated_at": datetime.now().isoformat(),
            "status": "READY"
        }}
        self.stats["generated"] += 1
        return payload

    def validate(self, payload: dict) -> bool:
        """Verify payload integrity."""
        expected = hashlib.sha256(
            json.dumps(payload.get("config", {{}}), sort_keys=True).encode()
        ).hexdigest()[:16]
        valid = expected == payload.get("checksum", "")
        if valid:
            self.stats["validated"] += 1
        return valid


def main():
    parser = argparse.ArgumentParser(description="{agent_name}")
    parser.add_argument("--config", help="JSON config for payload generation")
    parser.add_argument("--validate", help="JSON payload file to validate")
    parser.add_argument("--output", default="payload.json", help="Output file")
    args = parser.parse_args()

    engine = PayloadEngine()

    if args.config:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        payload = engine.generate(config)
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info(f"[GEN] Payload {{payload['id']}} -> {{args.output}}")
    elif args.validate:
        payload = json.loads(Path(args.validate).read_text(encoding="utf-8"))
        ok = engine.validate(payload)
        logger.info(f"[VALIDATE] {{payload.get('id','?')}}: {{'PASS' if ok else 'FAIL'}}")
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''

# ═══════════════════════════════════════════════════════════════════════════
# ROLE REGISTRY — maps every NEXUS role to its scaffold
# ═══════════════════════════════════════════════════════════════════════════
ROLE_SCAFFOLDS = {
    "collector":     SCAFFOLD_COLLECTOR,
    "processor":     SCAFFOLD_PROCESSOR,
    "analyzer":      SCAFFOLD_ANALYZER,
    "orchestrator":  SCAFFOLD_ORCHESTRATOR,
    "storage":       SCAFFOLD_STORAGE,
    "presentation":  SCAFFOLD_PRESENTATION,
    "library":       SCAFFOLD_LIBRARY,
    "payload":       SCAFFOLD_PAYLOAD,
}


def generate_scaffold(request: dict) -> str:
    """Generate a code scaffold from a synthesis request (REQ_*.json)."""
    child_id  = request["child_id"]
    parent_a  = request.get("parent_a", {})
    parent_b  = request.get("parent_b", {})
    mission   = request.get("mission", "")

    traits_a   = parent_a.get("evolution_matrix", {}).get("traits_fixed", {})
    role       = traits_a.get("role", "collector")
    security   = traits_a.get("security_level", "none")
    interface  = traits_a.get("interface", "cli")
    
    # Enhance 1: Auto-Track Generation
    gen_a = parent_a.get("evolution_matrix", {}).get("lineage", {}).get("generation", 0)
    gen_b = parent_b.get("evolution_matrix", {}).get("lineage", {}).get("generation", 0)
    gen = max(gen_a, gen_b) + 1

    # Enhance 2: Extract Domains for Context Injection
    domain_a = traits_a.get("domain", "misc")
    domain_b = parent_b.get("evolution_matrix", {}).get("traits_fixed", {}).get("domain", "misc")
    domains = f"{domain_a} & {domain_b}"

    template = ROLE_SCAFFOLDS.get(role, SCAFFOLD_COLLECTOR)

    return template.format(
        agent_name=child_id,
        mission=mission,
        parent_a=parent_a.get("node_id", "?"),
        parent_b=parent_b.get("node_id", "?"),
        role=role,
        security=security,
        interface=interface,
        generation=gen,
        domains=domains,
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: DNA_21_Scaffold_Generator.py <REQ_file.json>")
        print(f"\nSupported roles: {', '.join(ROLE_SCAFFOLDS.keys())}")
        sys.exit(1)

    req_path = Path(sys.argv[1])
    if not req_path.exists():
        print(f"[ERR] File not found: {req_path}")
        sys.exit(1)

    request = json.loads(req_path.read_text(encoding="utf-8"))
    scaffold = generate_scaffold(request)

    out_name = f"{request['child_id']}_scaffold.py"
    out_path = DNA_DIR / "DNA_12_AST_RENDER" / out_name
    out_path.write_text(scaffold, encoding="utf-8")
    print(f"[SCAFFOLD] Generated: {out_path}")
