You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: DOCKER_CONTAINER_MONITOR
Domain: INFRA
Purpose: Monitor running Docker containers for resource spikes and insecure port mappings

### Core Instructions & Data:
- Algorithm: Docker Engine API polling and resource threshold analysis
- API Targets:   - http://localhost:2375/containers/json?stats=1
- Data Model: {
    "container_id": "TEXT",
    "cpu_usage": "REAL",
    "mem_usage": "REAL",
    "exposed_ports": "TEXT",
    "is_healthy": "INTEGER"
}
- Input: keyword | Output: sqlite
- Required Modules:   - requests
  - logging
  - sqlite3
  - time
- Hardcoded Hooks:   - "docker.sock"
  - "container"
  - "stats"
  - "Networks"
  - "Ports"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: DockerContainerMonitorAgent | Table: docker_container_monitor | Main Method: execute_scan(self, target: str) -> DockerContainerMonitorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to DOCKER_CONTAINER_MONITOR logic.
