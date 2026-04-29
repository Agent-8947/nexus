#!/usr/bin/env python3
"""
NEXUS DNA Synthesis Protocol v2.0 — Spec-Driven Unique Agent Factory

Problem: LLMs (especially Flash-tier) produce identical boilerplate when
given similar prompts. Even with different agent names, the logic is copy-pasted.

Solution: Three-layer uniqueness enforcement:
  1. SPEC CONTRACT — unique JSON spec per agent (API, data model, algorithms)
  2. PROMPT INJECTION — spec is embedded into the generation prompt
  3. POST-SYNTHESIS VALIDATOR — AST-level structural comparison rejects clones

Usage:
  python synth_protocol_v2.py --domain OSINT --count 5
  python synth_protocol_v2.py --spec specs/my_agent.json
  python synth_protocol_v2.py --validate DNA_OSINT/
"""

import ast
import hashlib
import json
import logging
import sys
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SYNTH_PROTOCOL_V2")

DNA_ROOT = Path(__file__).resolve().parent
SPECS_DIR = DNA_ROOT / "agent_specs"
SPECS_DIR.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# LAYER 1: Agent Spec Contract
# ═══════════════════════════════════════════════════════════════

@dataclass
class AgentSpec:
    """Unique contract that defines what an agent MUST implement.
    No two specs can share the same (api_endpoint + data_model + algorithm)."""
    
    agent_id: str
    domain: str
    purpose: str  # One-line: what the agent does
    
    # UNIQUE differentiators — these MUST differ between agents
    api_endpoints: list[str]        # Real URLs the agent hits
    data_model: dict                # SQLite schema fields (column: type)
    core_algorithm: str             # Name of the main algorithm/technique
    input_type: str                 # "domain", "ip", "email", "file", "keyword", "asn"
    output_format: str              # "json_report", "csv", "sqlite", "graphml"
    
    # Required libraries (must appear in generated code)
    required_imports: list[str] = field(default_factory=list)
    
    # Domain-specific logic markers (strings that MUST appear in code)
    logic_markers: list[str] = field(default_factory=list)
    
    # Anti-clone: structural fingerprint
    spec_hash: str = ""
    
    def compute_hash(self) -> str:
        """Deterministic hash of the spec's unique differentiators."""
        unique_blob = json.dumps({
            "api": sorted(self.api_endpoints),
            "model": self.data_model,
            "algo": self.core_algorithm,
            "input": self.input_type,
        }, sort_keys=True)
        self.spec_hash = hashlib.sha256(unique_blob.encode()).hexdigest()[:16]
        return self.spec_hash


# ═══════════════════════════════════════════════════════════════
# LAYER 2: Spec Registry (prevents duplicate specs)
# ═══════════════════════════════════════════════════════════════

class SpecRegistry:
    """Manages agent specs and enforces uniqueness at the spec level."""
    
    def __init__(self, specs_dir: Path = SPECS_DIR):
        self.specs_dir = specs_dir
        self.specs_dir.mkdir(exist_ok=True)
        self._index: dict[str, AgentSpec] = {}
        self._load_existing()
    
    def _load_existing(self) -> None:
        for spec_file in self.specs_dir.glob("*.json"):
            try:
                data = json.loads(spec_file.read_text(encoding="utf-8"))
                spec = AgentSpec(**data)
                spec.compute_hash()
                self._index[spec.spec_hash] = spec
            except (json.JSONDecodeError, TypeError) as exc:
                logger.warning("Invalid spec file %s: %s", spec_file.name, exc)
        logger.info("Loaded %d existing specs", len(self._index))
    
    def register(self, spec: AgentSpec) -> bool:
        """Register a new spec. Returns False if a duplicate exists."""
        spec.compute_hash()
        
        if spec.spec_hash in self._index:
            existing = self._index[spec.spec_hash]
            logger.error(
                "DUPLICATE SPEC REJECTED: '%s' clashes with '%s' (hash: %s)",
                spec.agent_id, existing.agent_id, spec.spec_hash
            )
            return False
        
        # Check API endpoint overlap (>50% shared endpoints = clone)
        for existing in self._index.values():
            overlap = set(spec.api_endpoints) & set(existing.api_endpoints)
            if len(overlap) > len(spec.api_endpoints) * 0.5:
                logger.error(
                    "API OVERLAP REJECTED: '%s' shares %d/%d endpoints with '%s'",
                    spec.agent_id, len(overlap), len(spec.api_endpoints), existing.agent_id
                )
                return False
        
        # Save
        self._index[spec.spec_hash] = spec
        spec_path = self.specs_dir / f"{spec.agent_id}.json"
        spec_path.write_text(
            json.dumps(asdict(spec), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info("Registered spec: %s (hash: %s)", spec.agent_id, spec.spec_hash)
        return True
    
    def get_all(self) -> list[AgentSpec]:
        return list(self._index.values())


# ═══════════════════════════════════════════════════════════════
# LAYER 3: Post-Synthesis Uniqueness Validator
# ═══════════════════════════════════════════════════════════════

class UniquenessValidator:
    """AST-level structural comparison to detect code clones after synthesis."""
    
    @staticmethod
    def extract_structure(code: str) -> dict:
        """Extract structural fingerprint from Python code via AST."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "SyntaxError"}
        
        fingerprint = {
            "classes": [],
            "methods": [],
            "imports": [],
            "api_urls": [],
            "sql_tables": [],
            "string_literals": set(),
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fingerprint["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                fingerprint["methods"].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    fingerprint["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                fingerprint["imports"].append(node.module)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                val = node.value.strip()
                # Detect URLs
                if val.startswith("http://") or val.startswith("https://"):
                    fingerprint["api_urls"].append(val)
                # Detect SQL table names
                if "CREATE TABLE" in val.upper():
                    import re
                    match = re.search(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?(\w+)', val, re.IGNORECASE)
                    if match:
                        fingerprint["sql_tables"].append(match.group(1))
        
        # Convert set to sorted list for hashing
        fingerprint["string_literals"] = []
        return fingerprint
    
    @staticmethod
    def structural_hash(fingerprint: dict) -> str:
        """Hash the structural fingerprint."""
        normalized = json.dumps({
            "methods": sorted(fingerprint.get("methods", [])),
            "api_urls": sorted(fingerprint.get("api_urls", [])),
            "sql_tables": sorted(fingerprint.get("sql_tables", [])),
        }, sort_keys=True)
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    @staticmethod
    def similarity_score(fp1: dict, fp2: dict) -> float:
        """Calculate structural similarity between two fingerprints. 0.0=unique, 1.0=clone."""
        if not fp1 or not fp2:
            return 0.0
        
        methods1 = set(fp1.get("methods", []))
        methods2 = set(fp2.get("methods", []))
        urls1 = set(fp1.get("api_urls", []))
        urls2 = set(fp2.get("api_urls", []))
        tables1 = set(fp1.get("sql_tables", []))
        tables2 = set(fp2.get("sql_tables", []))
        
        scores = []
        
        # Method name similarity
        if methods1 or methods2:
            union = methods1 | methods2
            intersection = methods1 & methods2
            scores.append(len(intersection) / len(union) if union else 0)
        
        # API URL similarity (most important)
        if urls1 or urls2:
            union = urls1 | urls2
            intersection = urls1 & urls2
            url_sim = len(intersection) / len(union) if union else 0
            scores.append(url_sim * 2)  # Double weight for API URLs
        
        # SQL table similarity
        if tables1 or tables2:
            union = tables1 | tables2
            intersection = tables1 & tables2
            scores.append(len(intersection) / len(union) if union else 0)
        
        return min(1.0, sum(scores) / max(len(scores), 1))
    
    def validate_directory(self, directory: Path, threshold: float = 0.7) -> list[dict]:
        """Scan all .py files in directory and find clone pairs above threshold."""
        files: list[tuple[str, dict]] = []
        
        for py_file in sorted(directory.glob("*.py")):
            code = py_file.read_text(encoding="utf-8", errors="ignore")
            fp = self.extract_structure(code)
            files.append((py_file.name, fp))
        
        clones: list[dict] = []
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                sim = self.similarity_score(files[i][1], files[j][1])
                if sim >= threshold:
                    clones.append({
                        "file_a": files[i][0],
                        "file_b": files[j][0],
                        "similarity": round(sim, 3),
                        "verdict": "CLONE" if sim > 0.85 else "SUSPICIOUS",
                    })
        
        return clones


# ═══════════════════════════════════════════════════════════════
# PROMPT GENERATOR — Creates LLM prompt from spec
# ═══════════════════════════════════════════════════════════════

class PromptGenerator:
    """Generates a unique, spec-bound prompt for any LLM (Gemini Flash, Claude, etc.)."""
    
    TEMPLATE = """You are a NEXUS DNA agent synthesizer. Generate a COMPLETE, PRODUCTION-READY Python agent.

## MANDATORY SPEC CONTRACT (violation = rejection)

Agent ID: {agent_id}
Domain: {domain}
Purpose: {purpose}

### REQUIRED API Endpoints (you MUST use these exact URLs):
{api_endpoints}

### REQUIRED Data Model (SQLite table columns):
{data_model}

### REQUIRED Core Algorithm: {core_algorithm}
### Input Type: {input_type}
### Output Format: {output_format}

### REQUIRED Imports:
{required_imports}

### Logic Markers (these strings MUST appear in your code):
{logic_markers}

## STRUCTURAL REQUIREMENTS:
1. Use @dataclass for all data structures
2. logging.basicConfig with structured format — NO print() for output
3. sqlite3 persistence with parameterized queries
4. hashlib.sha256 for all data hashing
5. requests.Session() with retry logic and rate-limit handling (time.sleep in backoff context)
6. try/except with SPECIFIC exception types (no bare except)
7. Type hints on all function signatures
8. API keys from os.environ ONLY — never hardcode
9. if __name__ == "__main__" with sys.argv CLI
10. UNIQUE class name, method names, and table names — DO NOT copy from other agents

## ANTI-CLONE RULES:
- Your execute_scan() method MUST implement logic SPECIFIC to {core_algorithm}
- Your SQLite table MUST have columns matching the data model above
- Your HTTP requests MUST target the endpoints listed above
- Generic boilerplate without domain-specific logic will be REJECTED

Spec Hash: {spec_hash} (embed this in a comment at the top of the file)
"""
    
    @classmethod
    def generate(cls, spec: AgentSpec) -> str:
        spec.compute_hash()
        return cls.TEMPLATE.format(
            agent_id=spec.agent_id,
            domain=spec.domain,
            purpose=spec.purpose,
            api_endpoints="\n".join(f"  - {url}" for url in spec.api_endpoints),
            data_model=json.dumps(spec.data_model, indent=4),
            core_algorithm=spec.core_algorithm,
            input_type=spec.input_type,
            output_format=spec.output_format,
            required_imports="\n".join(f"  - {imp}" for imp in spec.required_imports),
            logic_markers="\n".join(f"  - \"{m}\"" for m in spec.logic_markers),
            spec_hash=spec.spec_hash,
        )


# ═══════════════════════════════════════════════════════════════
# OSINT SPEC LIBRARY — Pre-built unique specs
# ═══════════════════════════════════════════════════════════════

OSINT_SPEC_LIBRARY: list[dict] = [
    {
        "agent_id": "SHODAN_DEVICE_SCANNER",
        "domain": "OSINT",
        "purpose": "Discover internet-connected devices and open ports via Shodan InternetDB",
        "api_endpoints": ["https://internetdb.shodan.io/{ip}"],
        "data_model": {"ip": "TEXT", "ports": "TEXT", "hostnames": "TEXT", "cpes": "TEXT", "vulns": "TEXT", "tags": "TEXT"},
        "core_algorithm": "Shodan InternetDB passive reconnaissance",
        "input_type": "ip",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json", "dataclasses"],
        "logic_markers": ["internetdb.shodan.io", "cpes", "vulns"],
    },
    {
        "agent_id": "GITHUB_SECRET_SCANNER",
        "domain": "OSINT",
        "purpose": "Search GitHub code for leaked secrets, API keys, and credentials",
        "api_endpoints": ["https://api.github.com/search/code"],
        "data_model": {"query": "TEXT", "repo_full_name": "TEXT", "file_path": "TEXT", "match_snippet": "TEXT", "secret_type": "TEXT"},
        "core_algorithm": "GitHub Code Search API with regex secret patterns",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "re", "os"],
        "logic_markers": ["search/code", "GITHUB_TOKEN", "secret_type"],
    },
    {
        "agent_id": "PASTEBIN_INTEL_MONITOR",
        "domain": "OSINT",
        "purpose": "Monitor public paste services for leaked data mentioning target keywords",
        "api_endpoints": ["https://psbdmp.ws/api/v3/search/{query}"],
        "data_model": {"keyword": "TEXT", "paste_id": "TEXT", "paste_url": "TEXT", "content_preview": "TEXT", "source": "TEXT"},
        "core_algorithm": "PSBDMP paste dump search with keyword correlation",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json"],
        "logic_markers": ["psbdmp.ws", "paste_id", "content_preview"],
    },
    {
        "agent_id": "THREAT_INTEL_FEED",
        "domain": "OSINT",
        "purpose": "Aggregate indicators of compromise (IoCs) from public threat intelligence feeds",
        "api_endpoints": [
            "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
            "https://urlhaus-api.abuse.ch/v1/",
        ],
        "data_model": {"indicator": "TEXT", "indicator_type": "TEXT", "source": "TEXT", "pulse_count": "INTEGER", "threat_score": "REAL", "tags": "TEXT"},
        "core_algorithm": "Multi-source IoC correlation (AlienVault OTX + URLhaus)",
        "input_type": "ip",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json", "dataclasses"],
        "logic_markers": ["otx.alienvault.com", "urlhaus-api.abuse.ch", "pulse_count", "indicator_type"],
    },
    {
        "agent_id": "EMAIL_REPUTATION_PROFILER",
        "domain": "OSINT",
        "purpose": "Build reputation profile for email addresses using Disify and EmailRep APIs",
        "api_endpoints": [
            "https://disify.com/api/email/{email}",
            "https://emailrep.io/{email}",
        ],
        "data_model": {"email": "TEXT", "is_disposable": "INTEGER", "domain_age_days": "INTEGER", "reputation": "TEXT", "suspicious": "INTEGER", "profiles_found": "TEXT"},
        "core_algorithm": "Multi-source email reputation scoring (Disify disposable check + EmailRep profile)",
        "input_type": "email",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json"],
        "logic_markers": ["disify.com", "emailrep.io", "is_disposable", "reputation"],
    },
    {
        "agent_id": "TECHNOLOGY_PROFILER",
        "domain": "OSINT",
        "purpose": "Detect web technologies, frameworks, and CMS used by a target website",
        "api_endpoints": [
            "https://api.wappalyzer.com/v2/lookup/?urls={url}",
        ],
        "data_model": {"target_url": "TEXT", "technology": "TEXT", "category": "TEXT", "version": "TEXT", "confidence": "INTEGER"},
        "core_algorithm": "HTTP header + HTML meta + script fingerprinting",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "re", "json"],
        "logic_markers": ["X-Powered-By", "generator", "technology", "category"],
    },
    {
        "agent_id": "DNS_HISTORY_TRACKER",
        "domain": "OSINT",
        "purpose": "Track historical DNS record changes for a domain via SecurityTrails-compatible API",
        "api_endpoints": [
            "https://api.securitytrails.com/v1/domain/{domain}/dns/a/history",
        ],
        "data_model": {"domain": "TEXT", "record_type": "TEXT", "old_value": "TEXT", "new_value": "TEXT", "first_seen": "TEXT", "last_seen": "TEXT"},
        "core_algorithm": "DNS history diffing with temporal correlation",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "os", "json"],
        "logic_markers": ["securitytrails.com", "SECURITYTRAILS_API_KEY", "first_seen", "last_seen", "record_type"],
    },
    {
        "agent_id": "ASN_OWNERSHIP_MAPPER",
        "domain": "OSINT",
        "purpose": "Map organizational ownership of IP ranges via RIPE Stat and PeeringDB",
        "api_endpoints": [
            "https://stat.ripe.net/data/as-overview/data.json?resource={asn}",
            "https://www.peeringdb.com/api/net?asn={asn}",
        ],
        "data_model": {"asn": "INTEGER", "org_name": "TEXT", "holder": "TEXT", "country": "TEXT", "prefix_count": "INTEGER", "peering_policy": "TEXT", "ix_count": "INTEGER"},
        "core_algorithm": "Cross-referencing RIPE Stat AS overview with PeeringDB network records",
        "input_type": "asn",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json", "dataclasses"],
        "logic_markers": ["stat.ripe.net", "peeringdb.com", "peering_policy", "ix_count"],
    },
    {
        "agent_id": "FAVICON_HASH_HUNTER",
        "domain": "OSINT",
        "purpose": "Calculate favicon hashes (MurmurHash3) for correlation across Shodan/Censys",
        "api_endpoints": [
            "https://{domain}/favicon.ico",
        ],
        "data_model": {"domain": "TEXT", "favicon_url": "TEXT", "mmh3_hash": "INTEGER", "md5": "TEXT", "file_size": "INTEGER", "shodan_query": "TEXT"},
        "core_algorithm": "MurmurHash3 favicon fingerprinting for infrastructure correlation",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "base64", "struct"],
        "logic_markers": ["favicon.ico", "mmh3", "murmur", "http.favicon.hash"],
    },
    {
        "agent_id": "WAYBACK_SNAPSHOT_DIFFER",
        "domain": "OSINT",
        "purpose": "Compare historical website snapshots from Wayback Machine CDX API",
        "api_endpoints": [
            "https://web.archive.org/cdx/search/cdx?url={domain}&output=json",
            "https://web.archive.org/web/{timestamp}/{url}",
        ],
        "data_model": {"domain": "TEXT", "timestamp": "TEXT", "status_code": "INTEGER", "digest": "TEXT", "mime_type": "TEXT", "content_length": "INTEGER"},
        "core_algorithm": "Wayback CDX temporal diffing with content digest comparison",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib", "json"],
        "logic_markers": ["web.archive.org", "cdx/search", "timestamp", "digest"],
    },
]


# ═══════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

def cmd_register_specs():
    """Register all specs from the library."""
    registry = SpecRegistry()
    registered = 0
    for spec_data in OSINT_SPEC_LIBRARY:
        spec = AgentSpec(**spec_data)
        if registry.register(spec):
            registered += 1
    logger.info("Registered %d / %d specs", registered, len(OSINT_SPEC_LIBRARY))
    return registry


def cmd_generate_prompts():
    """Generate LLM prompts for all registered specs."""
    registry = SpecRegistry()
    prompts_dir = DNA_ROOT / "agent_prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    for spec in registry.get_all():
        prompt = PromptGenerator.generate(spec)
        prompt_path = prompts_dir / f"PROMPT_{spec.agent_id}.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        logger.info("Generated prompt: %s", prompt_path.name)
    
    logger.info("All prompts saved to: %s", prompts_dir)


def cmd_validate(directory: str):
    """Validate uniqueness of agents in a directory."""
    validator = UniquenessValidator()
    target = Path(directory)
    
    if not target.is_dir():
        logger.error("Not a directory: %s", directory)
        return
    
    clones = validator.validate_directory(target)
    
    if not clones:
        logger.info("PASS: No clones detected in %s", directory)
    else:
        logger.warning("CLONE PAIRS DETECTED:")
        for clone in clones:
            logger.warning(
                "  %s ↔ %s  (similarity: %.1f%% — %s)",
                clone["file_a"], clone["file_b"],
                clone["similarity"] * 100, clone["verdict"]
            )
    
    return clones


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
NEXUS DNA Synthesis Protocol v2.0

Commands:
  python synth_protocol_v2.py register     Register all specs (saves to agent_specs/)
  python synth_protocol_v2.py prompts      Generate LLM prompts (saves to agent_prompts/)
  python synth_protocol_v2.py validate <dir>  Check for code clones in directory
  python synth_protocol_v2.py full         Full pipeline: register + prompts + validate
""")
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "register":
        cmd_register_specs()
    elif cmd == "prompts":
        cmd_generate_prompts()
    elif cmd == "validate":
        target_dir = sys.argv[2] if len(sys.argv) > 2 else str(DNA_ROOT / "DNA_OSINT")
        cmd_validate(target_dir)
    elif cmd == "full":
        cmd_register_specs()
        cmd_generate_prompts()
        target_dir = sys.argv[2] if len(sys.argv) > 2 else str(DNA_ROOT / "DNA_OSINT")
        cmd_validate(target_dir)
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(1)
