#!/usr/bin/env python3
"""
NEXUS DNA Spec Expansion — Batch 1: SECURITY_ADV (10 Specs)
"""

import json
from pathlib import Path

# Paths
DNA_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA")
SPECS_DIR = DNA_ROOT / "agent_specs"
SPECS_DIR.mkdir(exist_ok=True)

SECURITY_ADV_SPECS = [
    {
        "agent_id": "CVE_EXPLOIT_MATCHER",
        "domain": "SECURITY_ADV",
        "purpose": "Match identified CVEs with publicly available exploit proof-of-concepts (PoCs)",
        "api_endpoints": ["https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve}", "https://api.github.com/search/repositories?q={cve}+exploit"],
        "data_model": {"cve_id": "TEXT", "exploit_url": "TEXT", "source": "TEXT", "stars": "INTEGER", "last_update": "TEXT"},
        "core_algorithm": "CVE-to-GitHub-PoC mapping with star-based relevance scoring",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["requests", "logging", "sqlite3", "re"],
        "logic_markers": ["cve.mitre.org", "exploit", "github.com/search/repositories"],
    },
    {
        "agent_id": "JWT_VULN_SCANNER",
        "domain": "SECURITY_ADV",
        "purpose": "Detect common JWT vulnerabilities: none-algorithm, weak secrets, and kid-injection",
        "api_endpoints": [],
        "data_model": {"token": "TEXT", "header": "TEXT", "payload": "TEXT", "vulnerabilities": "TEXT", "is_exploitable": "INTEGER"},
        "core_algorithm": "JWT header decoding and algorithm manipulation (HS256 -> none)",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["base64", "json", "hashlib", "logging", "re"],
        "logic_markers": ["eyJ", "alg", "none", "kid", "secret"],
    },
    {
        "agent_id": "SQL_INJECTION_FUZZER",
        "domain": "SECURITY_ADV",
        "purpose": "Identify potential SQL injection points via error-based and boolean-based fuzzing",
        "api_endpoints": ["{target_url}"],
        "data_model": {"url": "TEXT", "parameter": "TEXT", "payload": "TEXT", "response_diff": "REAL", "is_vulnerable": "INTEGER"},
        "core_algorithm": "Differential response analysis using time/boolean payloads",
        "input_type": "domain",
        "output_format": "sqlite",
        "required_imports": ["requests", "logging", "sqlite3", "time", "random"],
        "logic_markers": ["OR 1=1", "sleep(", "UNION SELECT", "syntax error"],
    },
    {
        "agent_id": "XSS_POLYGLOT_TESTER",
        "domain": "SECURITY_ADV",
        "purpose": "Test web inputs for Cross-Site Scripting (XSS) using advanced polyglot payloads",
        "api_endpoints": ["{target_url}"],
        "data_model": {"url": "TEXT", "payload": "TEXT", "reflection_context": "TEXT", "bypass_type": "TEXT", "confirmed": "INTEGER"},
        "core_algorithm": "Context-aware payload injection and DOM reflection tracking",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "re", "html"],
        "logic_markers": ["<script>", "onerror=", "javascript:", "polyglot"],
    },
    {
        "agent_id": "SUBDOMAIN_TAKEOVER_HUNTER",
        "domain": "SECURITY_ADV",
        "purpose": "Detect dangling DNS records (CNAME) pointing to unclaimed cloud services (S3, Heroku, etc.)",
        "api_endpoints": ["https://raw.githubusercontent.com/EdOverflow/can-i-take-over-xyz/master/fingerprints.json"],
        "data_model": {"subdomain": "TEXT", "cname": "TEXT", "service": "TEXT", "status": "TEXT", "vulnerable": "INTEGER"},
        "core_algorithm": "CNAME resolution and signature-based service mismatch detection",
        "input_type": "domain",
        "output_format": "sqlite",
        "required_imports": ["requests", "logging", "sqlite3", "socket"],
        "logic_markers": ["CNAME", "takeover", "NoSuchBucket", "Heroku", "S3"],
    },
    {
        "agent_id": "DOCKER_IMAGE_AUDITOR",
        "domain": "SECURITY_ADV",
        "purpose": "Scan Docker images for hardcoded secrets, insecure instructions, and root users",
        "api_endpoints": [],
        "data_model": {"image_name": "TEXT", "instruction": "TEXT", "severity": "TEXT", "finding": "TEXT", "file_path": "TEXT"},
        "core_algorithm": "Dockerfile/Image-layer regex analysis for credential patterns",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["re", "logging", "sqlite3", "json", "os"],
        "logic_markers": ["USER root", "ENV password", "ADD ", "FROM "],
    },
    {
        "agent_id": "SSL_TLS_CIPHER_AUDITOR",
        "domain": "SECURITY_ADV",
        "purpose": "Audit server SSL/TLS configurations for weak ciphers and protocols (SSLv3, TLS 1.0)",
        "api_endpoints": [],
        "data_model": {"host": "TEXT", "port": "INTEGER", "protocol": "TEXT", "cipher": "TEXT", "strength": "TEXT", "is_weak": "INTEGER"},
        "core_algorithm": "TCP handshake socket-level cipher negotiation scan",
        "input_type": "domain",
        "output_format": "sqlite",
        "required_imports": ["ssl", "socket", "logging", "sqlite3", "datetime"],
        "logic_markers": ["SSLContext", "PROTOCOL_TLS", "weak_ciphers", "handshake"],
    },
    {
        "agent_id": "AWS_S3_BUCKET_SCANNER",
        "domain": "SECURITY_ADV",
        "purpose": "Bruteforce and scan potentially misconfigured public S3 buckets",
        "api_endpoints": ["https://{bucket_name}.s3.amazonaws.com"],
        "data_model": {"bucket_name": "TEXT", "is_public": "INTEGER", "list_enabled": "INTEGER", "file_count": "INTEGER", "owner_id": "TEXT"},
        "core_algorithm": "HTTP XML-response parsing for ListBucketPermission results",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "xml.etree.ElementTree"],
        "logic_markers": ["s3.amazonaws.com", "ListBucketResult", "AccessDenied"],
    },
    {
        "agent_id": "MALWARE_MD5_CORRELATOR",
        "domain": "SECURITY_ADV",
        "purpose": "Correlate file hashes with known malware samples via VirusTotal-like APIs",
        "api_endpoints": ["https://mb-api.abuse.ch/api/v1/"],
        "data_model": {"md5": "TEXT", "label": "TEXT", "threat_type": "TEXT", "first_seen": "TEXT", "sha256": "TEXT"},
        "core_algorithm": "Bazaar Malware DB hash lookup and family correlation",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["requests", "logging", "sqlite3", "hashlib"],
        "logic_markers": ["abuse.ch/api", "get_info", "malware_family"],
    },
    {
        "agent_id": "GRAPHQL_INTROSPECTION_AUDITOR",
        "domain": "SECURITY_ADV",
        "purpose": "Scan GraphQL endpoints for enabled introspection and information disclosure",
        "api_endpoints": ["{target_url}"],
        "data_model": {"url": "TEXT", "introspection_enabled": "INTEGER", "type_count": "INTEGER", "schema_dump": "TEXT"},
        "core_algorithm": "GraphQL __schema query injection and response verification",
        "input_type": "domain",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "json"],
        "logic_markers": ["__schema", "introspection", "query", "graphql"],
    }
]

def main():
    for spec in SECURITY_ADV_SPECS:
        path = SPECS_DIR / f"{spec['agent_id']}.json"
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"Generated spec: {spec['agent_id']}")

if __name__ == "__main__":
    main()
