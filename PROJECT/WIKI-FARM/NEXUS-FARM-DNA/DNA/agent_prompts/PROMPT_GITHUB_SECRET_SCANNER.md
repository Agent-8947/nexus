You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: GITHUB_SECRET_SCANNER
Domain: OSINT
Purpose: Search GitHub code for leaked secrets, API keys, and credentials

### Core Instructions & Data:
- Algorithm: GitHub Code Search API with regex secret patterns
- API Targets:   - https://api.github.com/search/code
- Data Model: {
    "query": "TEXT",
    "repo_full_name": "TEXT",
    "file_path": "TEXT",
    "match_snippet": "TEXT",
    "secret_type": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - hashlib
  - re
  - os
- Hardcoded Hooks:   - "search/code"
  - "GITHUB_TOKEN"
  - "secret_type"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: GithubSecretScannerAgent | Table: github_secret_scanner | Main Method: execute_scan(self, target: str) -> GithubSecretScannerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to GITHUB_SECRET_SCANNER logic.
