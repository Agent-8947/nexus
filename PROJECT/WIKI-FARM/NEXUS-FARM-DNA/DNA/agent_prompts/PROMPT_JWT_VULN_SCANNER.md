You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: JWT_VULN_SCANNER
Domain: SECURITY_ADV
Purpose: Detect common JWT vulnerabilities: none-algorithm, weak secrets, and kid-injection

### Core Instructions & Data:
- Algorithm: JWT header decoding and algorithm manipulation (HS256 -> none)
- API Targets: 
- Data Model: {
    "token": "TEXT",
    "header": "TEXT",
    "payload": "TEXT",
    "vulnerabilities": "TEXT",
    "is_exploitable": "INTEGER"
}
- Input: keyword | Output: json_report
- Required Modules:   - base64
  - json
  - hashlib
  - logging
  - re
- Hardcoded Hooks:   - "eyJ"
  - "alg"
  - "none"
  - "kid"
  - "secret"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: JwtVulnScannerAgent | Table: jwt_vuln_scanner | Main Method: execute_scan(self, target: str) -> JwtVulnScannerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to JWT_VULN_SCANNER logic.
