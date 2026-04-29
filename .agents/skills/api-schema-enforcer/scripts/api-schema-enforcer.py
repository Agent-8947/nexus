#!/usr/bin/env python3
"""
API-SCHEMA-ENFORCER [NEXUS SYNTHESIZED v2.0]
Mission: Detect breaking changes in OpenAPI/Swagger specs and enforce backward compatibility
Role: validator | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("API-SCHEMA-ENFORCER")

# ── Breaking Change Definitions ──────────────────────────────────────────
BREAKING_CHANGES = {
    "endpoint_removed": {"severity": "CRITICAL", "description": "An existing endpoint was removed."},
    "field_removed": {"severity": "CRITICAL", "description": "A response field was removed."},
    "type_changed": {"severity": "CRITICAL", "description": "A field type was changed."},
    "required_added": {"severity": "HIGH", "description": "A new required field was added to request."},
    "method_changed": {"severity": "HIGH", "description": "HTTP method changed for an endpoint."},
    "response_code_removed": {"severity": "MEDIUM", "description": "A documented response code was removed."},
    "param_renamed": {"severity": "MEDIUM", "description": "A parameter was renamed."},
}
# ─────────────────────────────────────────────────────────────────────────


class SchemaDiffer:
    """Compares two OpenAPI specs and detects breaking changes."""

    def __init__(self):
        self.stats = {"breaking": 0, "warnings": 0, "additions": 0}

    def diff(self, old_spec: dict, new_spec: dict) -> list[dict]:
        findings = []
        old_paths = old_spec.get("paths", {})
        new_paths = new_spec.get("paths", {})

        # Detect removed endpoints
        for path in old_paths:
            if path not in new_paths:
                findings.append(self._finding("endpoint_removed", path, f"Endpoint {path} was removed entirely."))
                continue

            old_methods = set(old_paths[path].keys())
            new_methods = set(new_paths[path].keys())

            # Detect removed methods
            for method in old_methods - new_methods:
                if method.startswith("x-"):
                    continue
                findings.append(self._finding("method_changed", f"{method.upper()} {path}", f"Method {method.upper()} removed."))

            # Detect schema changes per method
            for method in old_methods & new_methods:
                if method.startswith("x-"):
                    continue
                findings.extend(self._diff_operation(path, method, old_paths[path][method], new_paths[path][method]))

        # Detect new endpoints (non-breaking, informational)
        for path in new_paths:
            if path not in old_paths:
                self.stats["additions"] += 1

        return findings

    def _diff_operation(self, path: str, method: str, old_op: dict, new_op: dict) -> list[dict]:
        findings = []
        label = f"{method.upper()} {path}"

        # Check removed response codes
        old_responses = set(old_op.get("responses", {}).keys())
        new_responses = set(new_op.get("responses", {}).keys())
        for code in old_responses - new_responses:
            findings.append(self._finding("response_code_removed", label, f"Response code {code} removed."))

        # Check required params added
        old_params = {p.get("name"): p for p in old_op.get("parameters", [])}
        new_params = {p.get("name"): p for p in new_op.get("parameters", [])}
        for name, param in new_params.items():
            if name not in old_params and param.get("required", False):
                findings.append(self._finding("required_added", label, f"New required param '{name}' added."))

        # Check removed params
        for name in old_params:
            if name not in new_params:
                findings.append(self._finding("param_renamed", label, f"Param '{name}' removed or renamed."))

        return findings

    def _finding(self, change_type: str, location: str, detail: str) -> dict:
        info = BREAKING_CHANGES.get(change_type, {"severity": "LOW", "description": change_type})
        is_breaking = info["severity"] in ("CRITICAL", "HIGH")
        if is_breaking:
            self.stats["breaking"] += 1
        else:
            self.stats["warnings"] += 1
        return {
            "type": change_type,
            "severity": info["severity"],
            "location": location,
            "detail": detail,
            "breaking": is_breaking,
        }


def main():
    parser = argparse.ArgumentParser(description="API-SCHEMA-ENFORCER: OpenAPI Breaking Change Detector")
    parser.add_argument("--old", required=True, help="Path to old (baseline) OpenAPI JSON spec")
    parser.add_argument("--new", required=True, help="Path to new (feature branch) OpenAPI JSON spec")
    parser.add_argument("--output", default="api_drift_report.json", help="Output report")
    parser.add_argument("--fail-on-breaking", action="store_true", help="Exit code 1 if breaking changes found")
    args = parser.parse_args()

    old_path = Path(args.old).resolve()
    new_path = Path(args.new).resolve()

    if not old_path.exists() or not new_path.exists():
        logger.error("One or both spec files not found.")
        sys.exit(1)

    old_spec = json.loads(old_path.read_text(encoding="utf-8"))
    new_spec = json.loads(new_path.read_text(encoding="utf-8"))

    differ = SchemaDiffer()
    findings = differ.diff(old_spec, new_spec)

    logger.info(f"[*] Breaking: {differ.stats['breaking']}, Warnings: {differ.stats['warnings']}, New endpoints: {differ.stats['additions']}")

    report = {
        "agent": "API-SCHEMA-ENFORCER",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "baseline": str(old_path),
        "candidate": str(new_path),
        "summary": {
            "breaking_changes": differ.stats["breaking"],
            "warnings": differ.stats["warnings"],
            "new_endpoints": differ.stats["additions"],
            "verdict": "BLOCKED" if differ.stats["breaking"] > 0 else "PASSED",
        },
        "findings": sorted(findings, key=lambda x: x["severity"]),
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Schema drift report -> {output}")

    if args.fail_on_breaking and differ.stats["breaking"] > 0:
        logger.error(f"PIPELINE BLOCKED: {differ.stats['breaking']} breaking change(s) detected.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
