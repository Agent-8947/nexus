You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: XSS_POLYGLOT_TESTER
Domain: SECURITY_ADV
Purpose: Test web inputs for Cross-Site Scripting (XSS) using advanced polyglot payloads

### Core Instructions & Data:
- Algorithm: Context-aware payload injection and DOM reflection tracking
- API Targets:   - {target_url}
- Data Model: {
    "url": "TEXT",
    "payload": "TEXT",
    "reflection_context": "TEXT",
    "bypass_type": "TEXT",
    "confirmed": "INTEGER"
}
- Input: domain | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - re
  - html
- Hardcoded Hooks:   - "<script>"
  - "onerror="
  - "javascript:"
  - "polyglot"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: XssPolyglotTesterAgent | Table: xss_polyglot_tester | Main Method: execute_scan(self, target: str) -> XssPolyglotTesterReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to XSS_POLYGLOT_TESTER logic.
