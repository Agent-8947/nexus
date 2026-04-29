You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: PROMPT_TEMPLATE_EVOLVER
Domain: AI_ML
Purpose: Iteratively mutate prompt templates to maximize model performance metrics

### Core Instructions & Data:
- Algorithm: Genetic algorithm-based prompt mutation loop
- API Targets: 
- Data Model: {
    "template_v1": "TEXT",
    "template_v2": "TEXT",
    "score_v1": "REAL",
    "score_v2": "REAL",
    "improvement": "REAL"
}
- Input: keyword | Output: sqlite
- Required Modules:   - logging
  - sqlite3
  - random
  - re
- Hardcoded Hooks:   - "evolution"
  - "mutation"
  - "template"
  - "fitness"
  - "score"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: PromptTemplateEvolverAgent | Table: prompt_template_evolver | Main Method: execute_scan(self, target: str) -> PromptTemplateEvolverReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to PROMPT_TEMPLATE_EVOLVER logic.
