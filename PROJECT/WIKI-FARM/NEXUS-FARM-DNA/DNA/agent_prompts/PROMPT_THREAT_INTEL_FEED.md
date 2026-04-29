You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: THREAT_INTEL_FEED
Domain: OSINT
Purpose: Aggregate indicators of compromise (IoCs) from public threat intelligence feeds

### Core Instructions & Data:
- Algorithm: Multi-source IoC correlation (AlienVault OTX + URLhaus)
- API Targets:   - https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general
  - https://urlhaus-api.abuse.ch/v1/
- Data Model: {
    "indicator": "TEXT",
    "indicator_type": "TEXT",
    "source": "TEXT",
    "pulse_count": "INTEGER",
    "threat_score": "REAL",
    "tags": "TEXT"
}
- Input: ip | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - hashlib
  - json
  - dataclasses
- Hardcoded Hooks:   - "otx.alienvault.com"
  - "urlhaus-api.abuse.ch"
  - "pulse_count"
  - "indicator_type"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: ThreatIntelFeedAgent | Table: threat_intel_feed | Main Method: execute_scan(self, target: str) -> ThreatIntelFeedReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to THREAT_INTEL_FEED logic.
