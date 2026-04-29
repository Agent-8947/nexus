You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: SUBDOMAIN_TAKEOVER_HUNTER
Domain: SECURITY_ADV
Purpose: Detect dangling DNS records (CNAME) pointing to unclaimed cloud services (S3, Heroku, etc.)

### Core Instructions & Data:
- Algorithm: CNAME resolution and signature-based service mismatch detection
- API Targets:   - https://raw.githubusercontent.com/EdOverflow/can-i-take-over-xyz/master/fingerprints.json
- Data Model: {
    "subdomain": "TEXT",
    "cname": "TEXT",
    "service": "TEXT",
    "status": "TEXT",
    "vulnerable": "INTEGER"
}
- Input: domain | Output: sqlite
- Required Modules:   - requests
  - logging
  - sqlite3
  - socket
- Hardcoded Hooks:   - "CNAME"
  - "takeover"
  - "NoSuchBucket"
  - "Heroku"
  - "S3"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: SubdomainTakeoverHunterAgent | Table: subdomain_takeover_hunter | Main Method: execute_scan(self, target: str) -> SubdomainTakeoverHunterReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to SUBDOMAIN_TAKEOVER_HUNTER logic.
