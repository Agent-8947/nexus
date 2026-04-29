You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: LLM_PROMPT_INJECTION_TESTER
Domain: AI_ML
Purpose: Test LLM applications for prompt injection vulnerabilities using adversarial payloads

### Core Instructions & Data:
- Algorithm: Adversarial prompt injection with pattern-based jailbreak detection
- API Targets:   - {target_llm_url}
- Data Model: {
    "payload": "TEXT",
    "response": "TEXT",
    "is_jailbroken": "INTEGER",
    "pattern_detected": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - re
  - json
- Hardcoded Hooks:   - "DAN mode"
  - "Ignore previous instructions"
  - "system prompt"
  - "jailbreak"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: LlmPromptInjectionTesterAgent | Table: llm_prompt_injection_tester | Main Method: execute_scan(self, target: str) -> LlmPromptInjectionTesterReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to LLM_PROMPT_INJECTION_TESTER logic.
