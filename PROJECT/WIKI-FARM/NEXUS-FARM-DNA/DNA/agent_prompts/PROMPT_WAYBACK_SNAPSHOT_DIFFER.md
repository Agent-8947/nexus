You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: WAYBACK_SNAPSHOT_DIFFER
Domain: OSINT
Purpose: Compare historical website snapshots from Wayback Machine CDX API

### Core Instructions & Data:
- Algorithm: Wayback CDX temporal diffing with content digest comparison
- API Targets:   - https://web.archive.org/cdx/search/cdx?url={domain}&output=json
  - https://web.archive.org/web/{timestamp}/{url}
- Data Model: {
    "domain": "TEXT",
    "timestamp": "TEXT",
    "status_code": "INTEGER",
    "digest": "TEXT",
    "mime_type": "TEXT",
    "content_length": "INTEGER"
}
- Input: domain | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - hashlib
  - json
- Hardcoded Hooks:   - "web.archive.org"
  - "cdx/search"
  - "timestamp"
  - "digest"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: WaybackSnapshotDifferAgent | Table: wayback_snapshot_differ | Main Method: execute_scan(self, target: str) -> WaybackSnapshotDifferReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to WAYBACK_SNAPSHOT_DIFFER logic.
