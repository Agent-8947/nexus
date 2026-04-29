You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: GITHUB_ACTIONS_SECURITY_SCANNER
Domain: INFRA
Purpose: Analyze GitHub Action workflows for insecure patterns (e.g. pull_request_target misuse)

### Core Instructions & Data:
- Algorithm: YAML AST analysis for insecure execution contexts and secret exposure
- API Targets:   - https://api.github.com/repos/{repo}/contents/.github/workflows
- Data Model: {
    "repo": "TEXT",
    "workflow": "TEXT",
    "trigger": "TEXT",
    "insecure_step": "TEXT",
    "severity": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - re
  - json
- Hardcoded Hooks:   - "pull_request_target"
  - "secrets."
  - "GITHUB_TOKEN"
  - "workflow"
  - "on:"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: GithubActionsSecurityScannerAgent | Table: github_actions_security_scanner | Main Method: execute_scan(self, target: str) -> GithubActionsSecurityScannerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to GITHUB_ACTIONS_SECURITY_SCANNER logic.
