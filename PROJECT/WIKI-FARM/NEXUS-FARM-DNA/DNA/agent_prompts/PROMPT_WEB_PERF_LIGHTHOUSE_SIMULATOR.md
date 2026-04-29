You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: WEB_PERF_LIGHTHOUSE_SIMULATOR
Domain: WEB
Purpose: Simulate basic Lighthouse performance metrics (LCP, CLS estimation) via Navigation Timing API

### Core Instructions & Data:
- Algorithm: HTTP response analysis and DOM-size-based performance heuristic
- API Targets:   - {domain}
- Data Model: {
    "url": "TEXT",
    "load_time_ms": "INTEGER",
    "dom_interactive_ms": "INTEGER",
    "page_size_kb": "INTEGER",
    "score": "REAL"
}
- Input: domain | Output: json_report
- Required Modules:   - requests
  - logging
  - time
  - re
- Hardcoded Hooks:   - "domInteractive"
  - "loadEventEnd"
  - "performance"
  - "timing"
  - "bytes"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: WebPerfLighthouseSimulatorAgent | Table: web_perf_lighthouse_simulator | Main Method: execute_scan(self, target: str) -> WebPerfLighthouseSimulatorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to WEB_PERF_LIGHTHOUSE_SIMULATOR logic.
