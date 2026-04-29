You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: NGINX_LOG_ANOMALY_DETECTOR
Domain: INFRA
Purpose: Analyze Nginx access logs for 4xx/5xx spikes and potential scrapers

### Core Instructions & Data:
- Algorithm: Log line regex parsing and sliding window frequency analysis
- API Targets: 
- Data Model: {
    "ip": "TEXT",
    "status_4xx_count": "INTEGER",
    "status_5xx_count": "INTEGER",
    "is_malicious": "INTEGER",
    "avg_latency": "REAL"
}
- Input: file | Output: sqlite
- Required Modules:   - re
  - logging
  - sqlite3
  - json
  - time
- Hardcoded Hooks:   - "access.log"
  - "404"
  - "500"
  - "remote_addr"
  - "request_time"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: NginxLogAnomalyDetectorAgent | Table: nginx_log_anomaly_detector | Main Method: execute_scan(self, target: str) -> NginxLogAnomalyDetectorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to NGINX_LOG_ANOMALY_DETECTOR logic.
