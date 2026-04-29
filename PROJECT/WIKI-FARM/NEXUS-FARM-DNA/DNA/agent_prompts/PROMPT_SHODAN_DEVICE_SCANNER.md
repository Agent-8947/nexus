You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: SHODAN_DEVICE_SCANNER
Domain: OSINT
Purpose: Discover internet-connected devices and open ports via Shodan InternetDB

### Core Instructions & Data:
- Algorithm: Shodan InternetDB passive reconnaissance
- API Targets:   - https://internetdb.shodan.io/{ip}
- Data Model: {
    "ip": "TEXT",
    "ports": "TEXT",
    "hostnames": "TEXT",
    "cpes": "TEXT",
    "vulns": "TEXT",
    "tags": "TEXT"
}
- Input: ip | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - hashlib
  - json
  - dataclasses
- Hardcoded Hooks:   - "internetdb.shodan.io"
  - "cpes"
  - "vulns"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: ShodanDeviceScannerAgent | Table: shodan_device_scanner | Main Method: execute_scan(self, target: str) -> ShodanDeviceScannerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to SHODAN_DEVICE_SCANNER logic.
