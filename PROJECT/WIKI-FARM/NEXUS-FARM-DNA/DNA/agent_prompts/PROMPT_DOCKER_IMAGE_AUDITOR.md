You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: DOCKER_IMAGE_AUDITOR
Domain: SECURITY_ADV
Purpose: Scan Docker images for hardcoded secrets, insecure instructions, and root users

### Core Instructions & Data:
- Algorithm: Dockerfile/Image-layer regex analysis for credential patterns
- API Targets: 
- Data Model: {
    "image_name": "TEXT",
    "instruction": "TEXT",
    "severity": "TEXT",
    "finding": "TEXT",
    "file_path": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - re
  - logging
  - sqlite3
  - json
  - os
- Hardcoded Hooks:   - "USER root"
  - "ENV password"
  - "ADD "
  - "FROM "

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: DockerImageAuditorAgent | Table: docker_image_auditor | Main Method: execute_scan(self, target: str) -> DockerImageAuditorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to DOCKER_IMAGE_AUDITOR logic.
