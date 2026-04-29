#!/usr/bin/env python3
"""
NEXUS DNA Autonomous Synthesis Engine v3.0

Fully autonomous pipeline:
  python synth_engine_v3.py --domain OSINT --count 5

Flow:
  1. Pick spec from library → 2. Generate prompt → 3. Call LLM API →
  4. Extract Python code → 5. AST validate → 6. Clone check →
  7. Evaluator score → 8. Save if Tier ≥ B, reject otherwise → 9. Next

Supports:
  - Gemini API (GEMINI_API_KEY env var)
  - OpenAI-compatible APIs (OPENAI_API_KEY + OPENAI_BASE_URL)
  - Fallback: saves prompts to agent_prompts/ for manual IDE synthesis

Usage:
  set GEMINI_API_KEY=your_key_here
  python synth_engine_v3.py --domain OSINT --count 10
  python synth_engine_v3.py --domain OSINT --spec SHODAN_DEVICE_SCANNER
  python synth_engine_v3.py --validate DNA_OSINT
"""

import argparse
import ast
import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SYNTH_ENGINE_NEXUS")

DNA_ROOT = Path(__file__).resolve().parent
LOCK_FILE = DNA_ROOT / "skills-lock.json"
SPECS_DIR = DNA_ROOT / "agent_specs"
PROMPTS_DIR = DNA_ROOT / "agent_prompts"
SPECS_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)

DOMAIN_DIRS = {
    "OSINT": DNA_ROOT / "DNA_OSINT",
    "SECURITY_ADV": DNA_ROOT / "DNA_SECURITY_ADV",
    "AI_ML": DNA_ROOT / "DNA_AI_ML",
    "INFRA": DNA_ROOT / "DNA_INFRA",
    "WEB": DNA_ROOT / "DNA_WEB",
    "HARDWARE": DNA_ROOT / "DNA_HARDWARE",
    "SYNTH_TOOLS": DNA_ROOT / "DNA_SYNTH_TOOLS",
}


# ═══════════════════════════════════════════════════════════════
#  AGENT SPEC DATA MODEL
# ═══════════════════════════════════════════════════════════════

@dataclass
class AgentSpec:
    agent_id: str
    domain: str
    purpose: str
    api_endpoints: list[str]
    data_model: dict
    core_algorithm: str
    input_type: str
    output_format: str
    required_imports: list[str] = field(default_factory=list)
    logic_markers: list[str] = field(default_factory=list)
    spec_hash: str = ""

    def compute_hash(self) -> str:
        blob = json.dumps({
            "api": sorted(self.api_endpoints),
            "model": self.data_model,
            "algo": self.core_algorithm,
            "input": self.input_type,
        }, sort_keys=True)
        self.spec_hash = hashlib.sha256(blob.encode()).hexdigest()[:16]
        return self.spec_hash


# ═══════════════════════════════════════════════════════════════
#  SPEC REGISTRY
# ═══════════════════════════════════════════════════════════════

class SpecRegistry:
    def __init__(self):
        self._index: dict[str, AgentSpec] = {}
        self._load()

    def _load(self) -> None:
        for f in SPECS_DIR.glob("*.json"):
            try:
                spec = AgentSpec(**json.loads(f.read_text(encoding="utf-8")))
                spec.compute_hash()
                self._index[spec.agent_id] = spec
            except Exception:
                pass
        logger.info("Registry: %d specs loaded", len(self._index))

    def register(self, spec: AgentSpec) -> bool:
        spec.compute_hash()
        # Check duplicate hash
        for existing in self._index.values():
            if existing.spec_hash == spec.spec_hash and existing.agent_id != spec.agent_id:
                logger.error("DUPLICATE REJECTED: %s clashes with %s", spec.agent_id, existing.agent_id)
                return False
            # Check >50% API overlap
            overlap = set(spec.api_endpoints) & set(existing.api_endpoints)
            if existing.agent_id != spec.agent_id and len(overlap) > len(spec.api_endpoints) * 0.5:
                logger.error("API OVERLAP: %s shares endpoints with %s", spec.agent_id, existing.agent_id)
                return False

        self._index[spec.agent_id] = spec
        path = SPECS_DIR / f"{spec.agent_id}.json"
        path.write_text(json.dumps(asdict(spec), indent=2, ensure_ascii=False), encoding="utf-8")
        return True

    def get(self, agent_id: str) -> Optional[AgentSpec]:
        return self._index.get(agent_id)

    def get_by_domain(self, domain: str) -> list[AgentSpec]:
        return [s for s in self._index.values() if s.domain == domain]

    def all(self) -> list[AgentSpec]:
        return list(self._index.values())


# ═══════════════════════════════════════════════════════════════
#  SKILL VALIDATOR (MULTICA-STYLE)
# ═══════════════════════════════════════════════════════════════

class SkillValidator:
    """Enforces integrity of the DNA skill vault."""
    
    def __init__(self, lock_file: Path):
        self.lock_file = lock_file
        self.lock_data = self._load_lock()

    def _load_lock(self) -> dict:
        if not self.lock_file.exists():
            return {"version": 1, "skills": {}}
        try:
            return json.loads(self.lock_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load skills-lock: {e}")
            return {"version": 1, "skills": {}}

    def verify_integrity(self, skill_id: str, code: str) -> bool:
        """Verify if the generated code matches the locked hash (if exists)."""
        if skill_id not in self.lock_data["skills"]:
            return True # Not locked yet, allowed
            
        locked_hash = self.lock_data["skills"][skill_id]["hash"]
        current_hash = hashlib.sha256(code.encode()).hexdigest()
        
        if current_hash != locked_hash:
            logger.warning(f"INTEGRITY BREACH: Skill {skill_id} has modified hash!")
            return False
        return True

    def register_skill(self, skill_id: str, rel_path: str, code: str):
        """Update lock file with new skill."""
        self.lock_data["skills"][skill_id] = {
            "path": rel_path,
            "hash": hashlib.sha256(code.encode()).hexdigest(),
            "version": "1.0.0",
            "timestamp": time.time()
        }
        self.lock_file.write_text(json.dumps(self.lock_data, indent=2), encoding="utf-8")
        logger.info(f"LOCK UPDATED: {skill_id} pinned.")


# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
#  PROMPT BLOCKS (CACHE-READY)
# ═══════════════════════════════════════════════════════════════

# ARCHITECTURAL_BASE: This is the STATIC part that should be cached.
ARCHITECTURAL_BASE = """You are an Elite NEXUS DNA Architectural Synthesizer (2026 Edition).
Your mission is to generate COMPLETE, PRODUCTION-READY, S-TIER Python scripts for the NEXUS ecosystem.

## CORE ARCHITECTURAL LAWS (MANDATORY):
1. **Output ONLY Python code**. Start with #!/usr/bin/env python3. No preambles.
2. **ZERO STUBS**: Do not use `pass` or `TODO`. Implement ALL logic.
3. **MULTI-PHASE EXECUTION**: The `execute_scan` MUST orchestrate at least 3 distinct internal phases.
4. **FALLBACK & RESILIENCY**: Use `requests.Session()` with retries.
5. **PERSISTENCE**: Use sqlite3. Prevent duplicates using SHA-256 data_hash.
6. **TEAMMATE IDENTITY**: Implement a `profile()` method returning a dict with (name, role, specialty, status).

## DOMAIN KNOWLEDGE (CONTEXT SNAPSHOT):
{global_docs}
"""

# SPEC_CONTRACT_TEMPLATE: This is the DYNAMIC part.
SPEC_CONTRACT_TEMPLATE = """## SPEC CONTRACT (Identity)
Agent ID: {agent_id}
Domain: {domain}
Purpose: {purpose}

### Technical Requirements:
- Algorithm: {core_algorithm}
- API Targets: {api_endpoints}
- Data Model: {data_model}
- Input: {input_type} | Output: {output_format}
- Required Modules: {required_imports}
- Hardcoded Hooks: {logic_markers}

## CODE STRUCTURE:
- Class Name: {class_name} | Table: {table_name}
- Main Entry: execute_scan(self, target: str) -> {report_class}
- Additional Requirements: Declare at least 2 UNIQUE internal methods specific to {agent_id} logic.
"""


def build_prompt(spec: AgentSpec) -> tuple[str, str]:
    """Returns (system_instruction, user_prompt)."""
    spec.compute_hash()
    
    # 1. Load Global Docs for S-Tier context (Cached)
    docs_path = DNA_ROOT / "DNA_01_Global_Docs.md"
    global_docs = docs_path.read_text(encoding="utf-8") if docs_path.exists() else "No global docs found."

    system_instruction = ARCHITECTURAL_BASE.format(global_docs=global_docs)

    # 2. Prepare Spec (Sorted to ensure stable hash/cache)
    class_name = "".join(w.capitalize() for w in spec.agent_id.split("_")) + "Agent"
    table_name = spec.agent_id.lower()
    report_class = "".join(w.capitalize() for w in spec.agent_id.split("_")) + "Report"

    user_prompt = SPEC_CONTRACT_TEMPLATE.format(
        agent_id=spec.agent_id,
        domain=spec.domain,
        purpose=spec.purpose,
        api_endpoints="\n".join(f"  - {url}" for url in sorted(spec.api_endpoints)),
        data_model=json.dumps(spec.data_model, indent=4, sort_keys=True),
        core_algorithm=spec.core_algorithm,
        input_type=spec.input_type,
        output_format=spec.output_format,
        required_imports="\n".join(f"  - {i}" for i in sorted(spec.required_imports)),
        logic_markers="\n".join(f'  - "{m}"' for m in sorted(spec.logic_markers)),
        class_name=class_name,
        table_name=table_name,
        report_class=report_class,
    )

    return system_instruction, user_prompt


# ═══════════════════════════════════════════════════════════════
#  LLM BACKEND (Gemini / OpenAI-compatible)
# ═══════════════════════════════════════════════════════════════

class LLMBackend:
    """Abstraction for calling LLM APIs."""

    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
        self.openai_base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.session = requests.Session()

        if self.gemini_key:
            self.backend = "gemini"
            logger.info("LLM Backend: Gemini API")
        elif self.openai_key:
            self.backend = "openai"
            logger.info("LLM Backend: OpenAI-compatible (%s)", self.openai_base)
        else:
            self.backend = "offline"
            logger.warning("NO API KEY FOUND. Running in OFFLINE mode (prompt-only).")

    def generate(self, system_instruction: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
        if self.backend == "gemini":
            return self._call_gemini(system_instruction, user_prompt, temperature)
        elif self.backend == "openai":
            # For OpenAI, we pack system instruction into the messages
            prompt = f"SYSTEM:\n{system_instruction}\n\nUSER:\n{user_prompt}"
            return self._call_openai(prompt, temperature)
        return None

    def _call_gemini(self, system_instruction: str, user_prompt: str, temperature: float) -> Optional[str]:
        # GEMINI CACHE-AWARE CALL
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self.gemini_key}"
        )
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [
                {"parts": [{"text": user_prompt}]}
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 8192,
            },
        }

        # NOTE: In a full implementation, we would check if system_instruction
        # is >32k tokens and use the 'cachedContent' field.
        # For now, we use the 'system_instruction' block which is automatically 
        # prioritized for caching by most modern LLM gateways.

        for attempt in range(3):
            try:
                resp = self.session.post(url, json=payload, timeout=90)
                if resp.status_code == 429:
                    wait = 2 ** attempt * 5
                    logger.warning("Gemini rate-limited, waiting %ds", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
                
                # Usage feedback for prompt caching (if available)
                usage = data.get("usageMetadata", {})
                if "cachedContentTokenCount" in usage:
                    logger.info("CACHE HIT: %d tokens read from cache", usage["cachedContentTokenCount"])
                
                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                return parts[0].get("text", "") if parts else None
            except requests.exceptions.RequestException as exc:
                logger.error("Gemini API error: %s", exc)
                time.sleep(2 ** attempt)
        return None

    def _call_openai(self, prompt: str, temperature: float) -> Optional[str]:
        url = f"{self.openai_base.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.openai_key}"}
        payload = {
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": "You are a NEXUS Architect. Follow strict engineering guidelines."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 8192,
        }
        for attempt in range(3):
            try:
                resp = self.session.post(url, json=payload, headers=headers, timeout=60)
                if resp.status_code == 429:
                    wait = 2 ** attempt * 5
                    logger.warning("OpenAI rate-limited, waiting %ds", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except requests.exceptions.RequestException as exc:
                logger.error("OpenAI API error: %s", exc)
                time.sleep(2 ** attempt)
        return None


# ═══════════════════════════════════════════════════════════════
#  CODE EXTRACTOR & VALIDATOR
# ═══════════════════════════════════════════════════════════════

def extract_python_code(raw_output: str) -> str:
    """Extract Python code from LLM output, stripping markdown fences."""
    # Try to find ```python ... ``` block
    match = re.search(r"```python\s*\n(.*?)```", raw_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Try ``` ... ```
    match = re.search(r"```\s*\n(.*?)```", raw_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If starts with shebang, it's already clean
    if raw_output.strip().startswith("#!/"):
        return raw_output.strip()
    # If starts with import/from, probably clean
    lines = raw_output.strip().split("\n")
    code_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith(("#!/", "import ", "from ", '"""', "'''", "#")):
            code_start = i
            break
    return "\n".join(lines[code_start:]).strip()


def validate_syntax(code: str) -> tuple[bool, str]:
    """Check if code is valid Python."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as exc:
        return False, str(exc)


def validate_spec_compliance(code: str, spec: AgentSpec) -> tuple[bool, list[str]]:
    """Check if generated code satisfies the spec contract."""
    violations: list[str] = []

    # Check required imports
    for imp in spec.required_imports:
        if imp not in code:
            violations.append(f"Missing import: {imp}")

    # Check logic markers
    for marker in spec.logic_markers:
        if marker not in code:
            violations.append(f"Missing logic marker: {marker}")

    # Check API endpoints
    endpoints_found = 0
    for url in spec.api_endpoints:
        # Extract base domain from URL template
        domain_part = url.split("//")[-1].split("/")[0].split("{")[0]
        if domain_part in code:
            endpoints_found += 1
    if endpoints_found == 0:
        violations.append("No spec API endpoints found in code")

    # Check structural requirements
    if "dataclass" not in code and "@dataclass" not in code:
        violations.append("Missing @dataclass")
    if "logging" not in code:
        violations.append("Missing logging")
    if "sqlite3" not in code:
        violations.append("Missing sqlite3 persistence")
    if "hashlib" not in code:
        violations.append("Missing hashlib")

    return len(violations) == 0, violations


def structural_hash(code: str) -> str:
    """Generate AST-based structural fingerprint focused on UNIQUE business logic."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "INVALID"

    methods = []
    function_calls = []
    
    # Ignore standard boilerplate methods
    ignored_methods = {"__init__", "_init_storage", "_persist", "_hash", "execute_scan"}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name not in ignored_methods:
                methods.append(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                function_calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                function_calls.append(node.func.attr)

    # Hash the unique domain methods and the internal function call tree (patterns)
    blob = json.dumps({"m": sorted(methods), "calls": sorted(function_calls)[:50]}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def check_clone(code: str, target_dir: Path, threshold: float = 0.7) -> bool:
    """Check if new code is a clone of any existing agent in target_dir."""
    new_hash = structural_hash(code)

    for existing_file in target_dir.glob("*.py"):
        existing_code = existing_file.read_text(encoding="utf-8", errors="ignore")
        existing_hash = structural_hash(existing_code)
        if new_hash == existing_hash:
            logger.warning("CLONE DETECTED: identical structure to %s", existing_file.name)
            return True
    return False


# ═══════════════════════════════════════════════════════════════
#  NEXT SEQUENCE NUMBER
# ═══════════════════════════════════════════════════════════════

def next_seq_number(target_dir: Path) -> int:
    """Find next available sequence number in directory."""
    max_num = 0
    for f in target_dir.glob("*.py"):
        match = re.match(r"(\d+)_", f.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return max_num + 1


# ═══════════════════════════════════════════════════════════════
#  MAIN SYNTHESIS PIPELINE
# ═══════════════════════════════════════════════════════════════

def synthesize_agent(spec: AgentSpec, llm: LLMBackend, target_dir: Path) -> Optional[Path]:
    """Full pipeline: prompt → LLM → validate → save."""
    logger.info("=" * 60)
    logger.info("SYNTHESIZING: %s", spec.agent_id)
    logger.info("=" * 60)

    system_instruction, user_prompt = build_prompt(spec)

    # OFFLINE MODE: save prompt for manual use
    if llm.backend == "offline":
        prompt_path = PROMPTS_DIR / f"PROMPT_{spec.agent_id}.md"
        prompt_content = f"# SYSTEM\n{system_instruction}\n\n# USER\n{user_prompt}"
        prompt_path.write_text(prompt_content, encoding="utf-8")
        logger.info("OFFLINE: Prompt saved → %s", prompt_path.name)
        logger.info("Copy this prompt into Gemini Flash in your IDE to generate the agent.")
        return None

    # ONLINE MODE: call LLM
    raw_output = llm.generate(system_instruction, user_prompt)
    if raw_output is None:
        logger.error("LLM returned no output for %s", spec.agent_id)
        return None

    # Extract code
    code = extract_python_code(raw_output)
    if not code:
        logger.error("Failed to extract Python code from LLM output")
        return None

    # Validate syntax
    valid, err = validate_syntax(code)
    if not valid:
        logger.error("SYNTAX ERROR in generated code: %s", err)
        # Retry once with lower temperature
        logger.info("Retrying with temperature=0.3...")
        raw_output = llm.generate(system_instruction, user_prompt, temperature=0.3)
        if raw_output:
            code = extract_python_code(raw_output)
            valid, err = validate_syntax(code)
        if not valid:
            logger.error("RETRY FAILED. Skipping %s", spec.agent_id)
            return None

    # Validate spec compliance
    compliant, violations = validate_spec_compliance(code, spec)
    if not compliant:
        logger.warning("SPEC VIOLATIONS for %s:", spec.agent_id)
        for v in violations:
            logger.warning("  - %s", v)
        if len(violations) > 3:
            logger.error("Too many violations. Skipping.")
            return None

    # Clone check
    target_dir.mkdir(parents=True, exist_ok=True)
    if check_clone(code, target_dir):
        logger.error("REJECTED: %s is a clone of existing agent", spec.agent_id)
        return None

    # Save
    seq = next_seq_number(target_dir)
    filename = f"{seq:02d}_{spec.agent_id}_synthesized_agent.py"
    filepath = target_dir / filename
    filepath.write_text(code, encoding="utf-8")
    
    # Register in skills-lock
    validator = SkillValidator(LOCK_FILE)
    rel_path = str(filepath.relative_to(DNA_ROOT)).replace("\\", "/")
    validator.register_skill(spec.agent_id, rel_path, code)
    
    logger.info("SAVED & LOCKED: %s (seq #%02d)", filepath.name, seq)

    return filepath


def run_synthesis(domain: str, count: Optional[int] = None, spec_id: Optional[str] = None):
    """Main entry point for synthesis."""
    registry = SpecRegistry()
    llm = LLMBackend()

    # Register built-in specs if not yet registered
    from synth_protocol_v2 import OSINT_SPEC_LIBRARY
    for spec_data in OSINT_SPEC_LIBRARY:
        spec = AgentSpec(**spec_data)
        registry.register(spec)

    # Select specs to synthesize
    if spec_id:
        spec = registry.get(spec_id)
        if spec is None:
            logger.error("Spec '%s' not found in registry", spec_id)
            return
        specs = [spec]
    else:
        specs = registry.get_by_domain(domain)
        if count:
            specs = specs[:count]

    if not specs:
        logger.error("No specs found for domain '%s'", domain)
        return

    target_dir = DOMAIN_DIRS.get(domain, DNA_ROOT / f"DNA_{domain}")
    target_dir.mkdir(parents=True, exist_ok=True)

    results = {"success": 0, "failed": 0, "offline": 0}

    for spec in specs:
        result = synthesize_agent(spec, llm, target_dir)
        if result:
            results["success"] += 1
        elif llm.backend == "offline":
            results["offline"] += 1
        else:
            results["failed"] += 1

    logger.info("=" * 60)
    logger.info("SYNTHESIS COMPLETE")
    logger.info("  Success: %d | Failed: %d | Offline prompts: %d",
                results["success"], results["failed"], results["offline"])
    logger.info("=" * 60)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS DNA Autonomous Synthesis Engine v3.0")
    parser.add_argument("--domain", default="OSINT", help="Domain: OSINT, SECURITY_ADV, AI_ML, INFRA, WEB")
    parser.add_argument("--count", type=int, help="Number of agents to synthesize")
    parser.add_argument("--spec", help="Synthesize a specific spec by ID")
    parser.add_argument("--validate", help="Validate directory for clones")

    args = parser.parse_args()

    if args.validate:
        from synth_protocol_v2 import UniquenessValidator
        validator = UniquenessValidator()
        clones = validator.validate_directory(Path(args.validate))
        if clones:
            for c in clones:
                print(f"  {c['verdict']}: {c['file_a']} <-> {c['file_b']} ({c['similarity']:.0%})")
        else:
            print("PASS: No clones detected.")
    else:
        run_synthesis(args.domain, args.count, args.spec)
