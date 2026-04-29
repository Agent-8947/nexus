You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: PASTEBIN_INTEL_MONITOR
Domain: OSINT
Purpose: Monitor public paste services for leaked data mentioning target keywords

### Core Instructions & Data:
- Algorithm: PSBDMP paste dump search with keyword correlation
- API Targets:   - https://psbdmp.ws/api/v3/search/{query}
- Data Model: {
    "keyword": "TEXT",
    "paste_id": "TEXT",
    "paste_url": "TEXT",
    "content_preview": "TEXT",
    "source": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - hashlib
  - json
- Hardcoded Hooks:   - "psbdmp.ws"
  - "paste_id"
  - "content_preview"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: PastebinIntelMonitorAgent | Table: pastebin_intel_monitor | Main Method: execute_scan(self, target: str) -> PastebinIntelMonitorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to PASTEBIN_INTEL_MONITOR logic.
