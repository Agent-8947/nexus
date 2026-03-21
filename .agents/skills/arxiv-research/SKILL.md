---
name: arxiv-research
description: |
  Search and retrieve academic papers from arXiv via free REST API.
  No API key, no dependencies — just curl / PowerShell Invoke-RestMethod.
  Also integrates Semantic Scholar for citations and related papers.

  USE FOR:
  - Searching AI/ML/CS papers on arXiv
  - Fetching paper abstracts and full PDFs
  - Generating BibTeX citations
  - Finding citations / references via Semantic Scholar
  - Author profile lookups
  - R&D research for NEXUS / AI capabilities studies

version: 1.0.0
author: NousResearch/hermes-agent (ported to NEXUS by Antigravity)
license: MIT
metadata:
  hermes:
    tags: [arxiv, research, papers, academic, ml, ai, semantic-scholar, bibtex]
    category: research
---

# arXiv Research

Search and retrieve academic papers from arXiv. No API key required.

## Quick Reference

| Action                  | Command                                                              |
|-------------------------|----------------------------------------------------------------------|
| Search papers           | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| Get specific paper      | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"`      |
| Read abstract (web)     | `firecrawl scrape "https://arxiv.org/abs/2402.03300"`               |
| Read full paper (PDF)   | `firecrawl scrape "https://arxiv.org/pdf/2402.03300"`               |

## 1. Searching Papers

```powershell
# Basic search — returns Atom XML
$query = "transformer attention mechanism"
$encoded = [uri]::EscapeDataString($query)
Invoke-RestMethod "https://export.arxiv.org/api/query?search_query=all:$encoded&max_results=5" | Out-String

# Clean readable output via Python
curl "https://export.arxiv.org/api/query?search_query=all:large+language+models&max_results=5" | python -c "
import sys, xml.etree.ElementTree as ET
ns = {'atom': 'http://www.w3.org/2005/Atom'}
root = ET.fromstring(sys.stdin.read())
for entry in root.findall('atom:entry', ns):
    title = entry.find('atom:title', ns).text.strip()
    arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
    published = entry.find('atom:published', ns).text[:10]
    print(f'[{arxiv_id}] ({published}) {title}')
"
```

## 2. Search Query Syntax

```
# Field prefixes
ti:transformer          # title
au:vaswani              # author
abs:attention           # abstract
cat:cs.LG               # category
all:keyword             # all fields

# Boolean operators
ti:GPT AND au:brown
ti:attention OR ti:transformer
ti:BERT ANDNOT au:devlin

# Examples
search_query=ti:mixture+of+experts+AND+cat:cs.LG
search_query=au:Yann+LeCun+AND+cat:cs.CV
```

## 3. Sort and Pagination

```powershell
# Sort: relevance | lastUpdatedDate | submittedDate
$url = "https://export.arxiv.org/api/query?search_query=all:rlhf&max_results=10&sortBy=submittedDate&sortOrder=descending&start=0"
Invoke-RestMethod $url
```

## 4. Fetch Specific Paper

```powershell
# Single paper by ID
Invoke-RestMethod "https://export.arxiv.org/api/query?id_list=2402.03300"

# Multiple papers
Invoke-RestMethod "https://export.arxiv.org/api/query?id_list=2402.03300,2310.06825,1706.03762"
```

## 5. BibTeX Generation

```powershell
# Extract BibTeX fields from API response
$paper_id = "1706.03762"  # "Attention Is All You Need"
$xml = Invoke-RestMethod "https://export.arxiv.org/api/query?id_list=$paper_id"
# Then format as BibTeX:
# @article{<first_author><year>,
#   title={<title>},
#   author={<authors>},
#   year={<year>},
#   eprint={<arxiv_id>},
#   archivePrefix={arXiv},
#   url={https://arxiv.org/abs/<arxiv_id>}
# }
```

## 6. Reading Paper Content

```powershell
# Abstract page (recommended — structured, no login needed)
firecrawl scrape "https://arxiv.org/abs/2402.03300" -o .firecrawl/paper-abstract.md

# Full PDF (text extraction, may be noisy)
firecrawl scrape "https://arxiv.org/pdf/2402.03300" -o .firecrawl/paper-full.md

# HTML version (cleaner than PDF when available)
firecrawl scrape "https://arxiv.org/html/2402.03300" -o .firecrawl/paper-html.md
```

## 7. Common Categories

| Category | Field                          |
|----------|-------------------------------|
| cs.AI    | Artificial Intelligence        |
| cs.LG    | Machine Learning               |
| cs.CL    | Computation & Language (NLP)   |
| cs.CV    | Computer Vision                |
| cs.NE    | Neural & Evolutionary Computing|
| stat.ML  | Statistics — Machine Learning  |
| cs.CR    | Cryptography & Security        |
| cs.IR    | Information Retrieval          |

## 8. Semantic Scholar (Citations & Related Papers)

```powershell
$SS_BASE = "https://api.semanticscholar.org/graph/v1"

# Paper details
Invoke-RestMethod "$SS_BASE/paper/arXiv:1706.03762?fields=title,authors,year,citationCount,abstract"

# Papers that CITE this paper
Invoke-RestMethod "$SS_BASE/paper/arXiv:1706.03762/citations?fields=title,authors,year&limit=10"

# Papers this paper REFERENCES
Invoke-RestMethod "$SS_BASE/paper/arXiv:1706.03762/references?fields=title,authors,year&limit=10"

# Paper recommendations (related papers)
Invoke-RestMethod -Method POST `
  -Uri "$SS_BASE/paper/recommendations" `
  -Body '{"positivePaperIds":["1706.03762"]}' `
  -ContentType "application/json"

# Author profile
Invoke-RestMethod "$SS_BASE/author/1741101?fields=name,affiliations,paperCount,citationCount,hIndex"
```

## 9. Complete Research Workflow

```powershell
# 1. Search for recent papers on a topic
$topic = "mixture of experts language model"
curl "https://export.arxiv.org/api/query?search_query=all:$([uri]::EscapeDataString($topic))&max_results=10&sortBy=submittedDate&sortOrder=descending"

# 2. Pick relevant paper IDs from results

# 3. Get full details + read abstract
firecrawl scrape "https://arxiv.org/abs/<chosen-id>" -o .firecrawl/paper.md

# 4. Find related work via Semantic Scholar
Invoke-RestMethod "https://api.semanticscholar.org/graph/v1/paper/arXiv:<chosen-id>/references?fields=title,year&limit=20"

# 5. Save BibTeX for citations
```

## Rate Limits

- **arXiv API**: 3 req/sec; use `Start-Sleep -Milliseconds 334` between bulk requests
- **Semantic Scholar**: ~100 req/5min (unauthenticated); add `x-api-key` header for higher limits

## Notes

- arxiv IDs change format: pre-2007 use `cs/0601001`; post-2007 use `2402.03300`
- Withdrawn papers still appear in API with retraction notice in abstract
- PDF text extraction quality varies — prefer HTML version when available (`/html/<id>`)

---
*Ported from NousResearch/hermes-agent by Antigravity NEXUS*
