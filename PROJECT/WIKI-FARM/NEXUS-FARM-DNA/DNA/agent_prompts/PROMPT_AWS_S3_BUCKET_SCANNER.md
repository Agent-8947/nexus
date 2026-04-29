You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: AWS_S3_BUCKET_SCANNER
Domain: SECURITY_ADV
Purpose: Bruteforce and scan potentially misconfigured public S3 buckets

### Core Instructions & Data:
- Algorithm: HTTP XML-response parsing for ListBucketPermission results
- API Targets:   - https://{bucket_name}.s3.amazonaws.com
- Data Model: {
    "bucket_name": "TEXT",
    "is_public": "INTEGER",
    "list_enabled": "INTEGER",
    "file_count": "INTEGER",
    "owner_id": "TEXT"
}
- Input: keyword | Output: json_report
- Required Modules:   - requests
  - logging
  - sqlite3
  - xml.etree.ElementTree
- Hardcoded Hooks:   - "s3.amazonaws.com"
  - "ListBucketResult"
  - "AccessDenied"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: AwsS3BucketScannerAgent | Table: aws_s3_bucket_scanner | Main Method: execute_scan(self, target: str) -> AwsS3BucketScannerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to AWS_S3_BUCKET_SCANNER logic.
