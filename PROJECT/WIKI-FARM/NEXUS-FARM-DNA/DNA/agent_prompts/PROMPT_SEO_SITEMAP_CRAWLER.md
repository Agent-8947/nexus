You are an Elite NEXUS DNA Architectural Synthesizer. 
Generate a COMPLETE, PRODUCTION-READY, S-TIER Python script.

RULES — VIOLATION = IMMEDIATE REJECTION:
1. Output ONLY Python code. No markdown fences. Start with #!/usr/bin/env python3
2. The code MUST run standalone. Do NOT use fake placeholder APIs if local tools/parsing can be used.

## SPEC CONTRACT (Identity)
Agent ID: SEO_SITEMAP_CRAWLER
Domain: WEB
Purpose: Crawl website sitemaps and audit for broken links (404) and missing meta tags

### Core Instructions & Data:
- Algorithm: XML sitemap parsing and concurrent link status checking
- API Targets:   - {domain}/sitemap.xml
- Data Model: {
    "url": "TEXT",
    "status_code": "INTEGER",
    "title": "TEXT",
    "meta_desc": "TEXT",
    "is_broken": "INTEGER"
}
- Input: domain | Output: sqlite
- Required Modules:   - requests
  - logging
  - sqlite3
  - re
  - xml.etree.ElementTree
- Hardcoded Hooks:   - "sitemap"
  - "loc"
  - "urlset"
  - "meta name="description""
  - "title"

## S-TIER ARCHITECTURE (MANDATORY):
1. **MULTI-PHASE EXECUTION**: Do not write a "thin wrapper". The `execute_scan` MUST orchestrate at least 3 distinct internal phases (e.g., `_recon()`, `_analyze()`, `_validate()`). You MUST invent deep, domain-specific logic.
2. **FALLBACK & RESILIENCY**: If an API fails or is missing, implement a fallback mechanism (e.g., local heuristic analysis, secondary OSINT source, mock simulation mode). Use `requests.Session()` with bounded retries.
3. **PERSISTENCE**: Use sqlite3 to cache/store results based on the Data Model. Protect against duplicates using a unique SHA-256 data_hash.

## ANTI-CLONE REQUIREMENTS
- Class Name: SeoSitemapCrawlerAgent | Table: seo_sitemap_crawler | Main Method: execute_scan(self, target: str) -> SeoSitemapCrawlerReport
- In addition to standard methods, you MUST declare at least 2 unique internal methods specific to SEO_SITEMAP_CRAWLER logic.
