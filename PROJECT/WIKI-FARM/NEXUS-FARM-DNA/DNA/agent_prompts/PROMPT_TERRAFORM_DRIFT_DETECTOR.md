You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: TERRAFORM_DRIFT_DETECTOR
Domain: INFRA
Purpose: Detect drift between local Terraform state and actual cloud resources via provider APIs

### Core Instructions & Data:
- Algorithm: State-to-API property diffing with fuzzy matching
- API Targets:   - https://{provider_api}.com/v1/resources
- Data Model: {
    "resource_id": "TEXT",
    "state_value": "TEXT",
    "actual_value": "TEXT",
    "drifted": "INTEGER"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - json
  - re
- Hardcoded Hooks:   - "terraform.tfstate"
  - "drift"
  - "managed"
  - "provider"
  - "attribute"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: TerraformDriftDetectorAgent | Table: terraform_drift_detector | Main Method: execute_scan(self, target: str) -> TerraformDriftDetectorReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to TERRAFORM_DRIFT_DETECTOR logic.
