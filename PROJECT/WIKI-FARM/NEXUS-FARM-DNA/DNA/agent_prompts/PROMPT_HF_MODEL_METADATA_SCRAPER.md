You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: HF_MODEL_METADATA_SCRAPER
Domain: AI_ML
Purpose: Fetch metadata, architectures, and performance metrics from HuggingFace models

### Core Instructions & Data:
- Algorithm: HuggingFace Hub API scraping and tag categorization
- API Targets:   - https://huggingface.co/api/models/{model_id}
- Data Model: {
    "model_id": "TEXT",
    "architecture": "TEXT",
    "downloads": "INTEGER",
    "likes": "INTEGER",
    "tags": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - json
- Hardcoded Hooks:   - "huggingface.co/api"
  - "modelId"
  - "transformers"
  - "pipeline_tag"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: HfModelMetadataScraperAgent | Table: hf_model_metadata_scraper | Main Method: execute_scan(self, target: str) -> HfModelMetadataScraperReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to HF_MODEL_METADATA_SCRAPER logic.
