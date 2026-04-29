#!/usr/bin/env python3
"""
NEXUS ROLE CONTRACTS v1.0
==========================
Each role ENFORCES a mandatory interface.
The composer generates code that IMPLEMENTS the interface,
not just writes the role name in a comment.

collector  → collect(target) → List[Finding]
analyzer   → analyze(findings: List[Finding]) → List[Finding]
storage    → insert(findings) / query(filter) → List[Finding]
processor  → process(data) → Dict[str, Any]
orchestrator → run_pipeline(target) → Report
library    → public functions only, no side-effects
payload    → execute(target) → Finding
presentation → render(report) → str
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class RoleContract:
    """Defines what a role MUST implement."""
    role: str
    required_method: str       # Main method name
    input_signature: str       # Python type annotation for input
    output_signature: str      # Python type annotation for output
    class_name: str            # Generated class name prefix
    docstring: str             # What this role does
    method_body_hint: str      # Skeleton for the method body
    test_assertion: str        # How to verify the contract in --test


ROLE_CONTRACTS: Dict[str, RoleContract] = {

    "collector": RoleContract(
        role="collector",
        required_method="collect",
        input_signature="target",
        output_signature="List[Dict[str, Any]]",
        class_name="Collector",
        docstring="Gathers raw data from target and returns standardized findings",
        method_body_hint="Run domain blocks, aggregate findings, return list",
        test_assertion='assert isinstance(result, list), "collect() must return list"',
    ),

    "analyzer": RoleContract(
        role="analyzer",
        required_method="analyze",
        input_signature="findings: List[Dict[str, Any]]",
        output_signature="List[Dict[str, Any]]",
        class_name="Analyzer",
        docstring="Takes findings from a collector, enriches/filters, returns refined findings",
        method_body_hint="Filter, score, deduplicate, enrich findings",
        test_assertion='assert isinstance(result, list), "analyze() must return list"',
    ),

    "storage": RoleContract(
        role="storage",
        required_method="insert",
        input_signature="findings: List[Dict[str, Any]]",
        output_signature="Dict[str, Any]",
        class_name="Store",
        docstring="Persists findings and provides query interface",
        method_body_hint="Store to SQLite, return summary stats",
        test_assertion='assert isinstance(result, dict) and "total_stored" in result',
    ),

    "processor": RoleContract(
        role="processor",
        required_method="process",
        input_signature="data: Any",
        output_signature="Dict[str, Any]",
        class_name="Processor",
        docstring="Transforms raw data into structured output",
        method_body_hint="Parse, transform, compute, return dict",
        test_assertion='assert isinstance(result, dict)',
    ),

    "orchestrator": RoleContract(
        role="orchestrator",
        required_method="run",
        input_signature="target",
        output_signature="Dict[str, Any]",
        class_name="Orchestrator",
        docstring="Coordinates multiple blocks in a pipeline",
        method_body_hint="Execute stages in order, collect results",
        test_assertion='assert isinstance(result, dict) and "findings" in result',
    ),

    "library": RoleContract(
        role="library",
        required_method="get_tools",
        input_signature="",
        output_signature="Dict[str, callable]",
        class_name="Toolkit",
        docstring="Provides reusable utility functions with no side-effects",
        method_body_hint="Return dict of {name: function}",
        test_assertion='assert isinstance(result, dict)',
    ),

    "payload": RoleContract(
        role="payload",
        required_method="execute",
        input_signature="target",
        output_signature="List[Dict[str, Any]]",
        class_name="Payload",
        docstring="Executes targeted action against target, returns findings",
        method_body_hint="Run targeted scan/check, return findings",
        test_assertion='assert isinstance(result, list)',
    ),

    "presentation": RoleContract(
        role="presentation",
        required_method="render",
        input_signature="report: Dict[str, Any]",
        output_signature="str",
        class_name="Renderer",
        docstring="Converts structured report into human-readable output",
        method_body_hint="Format findings as text/markdown/table",
        test_assertion='assert isinstance(result, str) and len(result) > 0',
    ),
}


def get_contract(role: str) -> RoleContract:
    """Get role contract, defaulting to orchestrator."""
    return ROLE_CONTRACTS.get(role, ROLE_CONTRACTS["orchestrator"])


def generate_role_class(contract: RoleContract, child_id: str, block_calls: str) -> str:
    """Generate a class that IMPLEMENTS the role contract."""

    if contract.role == "collector":
        return f'''
class {contract.class_name}:
    """{contract.docstring}"""

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {{}}
        self.errors: List[str] = []

    def collect(self, target) -> List[Dict[str, Any]]:
        """COLLECTOR CONTRACT: collect(target) → List[Finding]"""
        self.findings = []
        self.errors = []
{block_calls}
        return self.findings

    def summary(self) -> Dict[str, Any]:
        risk = {{"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}}
        for f in self.findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {{"total": len(self.findings), "errors": len(self.errors), "risk": risk, "stats": self.all_stats}}
'''

    elif contract.role == "analyzer":
        return f'''
class {contract.class_name}:
    """{contract.docstring}"""

    def __init__(self):
        self.enriched: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {{}}
        self.errors: List[str] = []

    def analyze(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ANALYZER CONTRACT: analyze(findings) → List[Finding]"""
        self.enriched = []
        self.errors = []
        # Deduplicate by (type, source)
        seen = set()
        for f in findings:
            key = (f.get("type", ""), f.get("source", ""))
            if key not in seen:
                seen.add(key)
                self.enriched.append(f)
        # Run analysis blocks
{block_calls}
        return self.enriched

    def summary(self) -> Dict[str, Any]:
        risk = {{"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}}
        for f in self.enriched:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {{"total": len(self.enriched), "errors": len(self.errors), "risk": risk, "stats": self.all_stats}}
'''

    elif contract.role == "storage":
        return f'''
class {contract.class_name}:
    """{contract.docstring}"""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = None
        self.all_stats: Dict[str, Any] = {{}}
        self.errors: List[str] = []

    def _get_conn(self):
        if self._conn is None:
            import sqlite3
            self._conn = sqlite3.connect(self.db_path)
            self._conn.execute("""CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT, severity TEXT, detail TEXT, source TEXT, ts TEXT, data TEXT
            )""")
        return self._conn

    def insert(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """STORAGE CONTRACT: insert(findings) → summary"""
        conn = self._get_conn()
        count = 0
        for f in findings:
            try:
                conn.execute("INSERT INTO findings (type, severity, detail, source, ts, data) VALUES (?,?,?,?,?,?)",
                    (f.get("type",""), f.get("severity",""), f.get("detail",""),
                     f.get("source",""), datetime.now().isoformat(), json.dumps(f)))
                count += 1
            except Exception as e:
                self.errors.append(str(e))
        conn.commit()
        return {{"total_stored": count, "errors": len(self.errors)}}

    def query(self, severity: str = None) -> List[Dict[str, Any]]:
        """STORAGE CONTRACT: query(filter) → List[Finding]"""
        conn = self._get_conn()
        if severity:
            rows = conn.execute("SELECT data FROM findings WHERE severity = ?", (severity,)).fetchall()
        else:
            rows = conn.execute("SELECT data FROM findings").fetchall()
        return [json.loads(r[0]) for r in rows]
'''

    elif contract.role == "presentation":
        return f'''
class {contract.class_name}:
    """{contract.docstring}"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {{}}
        self.errors: List[str] = []

    def render(self, report: Dict[str, Any]) -> str:
        """PRESENTATION CONTRACT: render(report) → str"""
        self.all_findings = report.get("findings", [])
        self.all_stats = report.get("stats", {{}})
{block_calls}
        # Final formatting: join all findings into a structured report
        output = [f"# {child_id} Analysis Report", f"Timestamp: {{datetime.now().isoformat()}}", ""]
        output.append("## Risk Summary")
        risk = {{"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        for k, v in risk.items():
            output.append(f"- {{k}}: {{v}}")
        
        output.append("\\n## Critical Findings")
        for f in [x for x in self.all_findings if x.get("severity") in ("CRITICAL", "HIGH")]:
            output.append(f"### [{{f.get('severity')}}] {{f.get('type')}}")
            output.append(f"- Detail: {{f.get('detail')}}")
            output.append(f"- Source: {{f.get('source')}}")

        return "\\n".join(output)
'''

    else:  # orchestrator / processor / payload / library
        return f'''
class {contract.class_name}:
    """{contract.docstring}"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {{}}
        self.errors: List[str] = []

    def {contract.required_method}(self, target) -> {contract.output_signature}:
        """{contract.role.upper()} CONTRACT: {contract.required_method}(target) → {contract.output_signature}"""
{block_calls}
        risk = {{"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {{
            "agent": "{child_id}",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }}
'''


if __name__ == "__main__":
    for role, contract in ROLE_CONTRACTS.items():
        print(f"  {role:15s} -> {contract.required_method}({contract.input_signature}) -> {contract.output_signature}")
    print(f"[OK] {len(ROLE_CONTRACTS)} role contracts defined")
