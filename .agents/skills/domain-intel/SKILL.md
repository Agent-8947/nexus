---
name: domain-intel
description: |
  Passive domain reconnaissance — subdomains, SSL certs, WHOIS, DNS records, domain availability.
  Zero dependencies, zero API keys. Pure Python stdlib. Works on Windows, Linux, macOS.

  USE FOR:
  - Subdomain discovery via Certificate Transparency logs (crt.sh)
  - SSL certificate inspection (expiry, cipher, SANs, issuer)
  - WHOIS lookup (registrar, registration dates, name servers)
  - DNS records (A, AAAA, MX, NS, TXT, CNAME)
  - Domain availability checks (passive: DNS + WHOIS + SSL signals)
  - Bulk multi-domain analysis
  - INTEL-SIGHT OSINT investigations (corporate domain mapping)

version: 1.1.0
author: NousResearch/hermes-agent (ported to NEXUS by Antigravity)
license: MIT
metadata:
  hermes:
    tags: [osint, domain, dns, whois, ssl, recon, intel-sight]
    category: research
    related_skills: [firecrawl]
---

# Domain Intelligence — Passive OSINT

Passive domain reconnaissance using only Python stdlib.
**Zero dependencies. Zero API keys. Works on Windows (PowerShell + Python).**

## When to Use

- User asks: "найди поддомены example.com", "проверь SSL сертификат", "кому принадлежит домен"
- INTEL-SIGHT task: mapping corporate infrastructure
- Checking domain availability before registering
- Passive pre-engagement recon before OSINT investigation

## Helper Script

This skill includes `scripts/domain_intel.py`. Run via:

```powershell
# Windows PowerShell — Subdomain discovery via Certificate Transparency logs
python "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\.agents\skills\domain-intel\scripts\domain_intel.py" subdomains example.com

# SSL certificate inspection (expiry, cipher, SANs, issuer)
python "...skills\domain-intel\scripts\domain_intel.py" ssl example.com

# WHOIS lookup (registrar, dates, name servers — 100+ TLDs)
python "...skills\domain-intel\scripts\domain_intel.py" whois example.com

# DNS records (A, AAAA, MX, NS, TXT, CNAME)
python "...skills\domain-intel\scripts\domain_intel.py" dns example.com

# Domain availability check (passive: DNS + WHOIS + SSL signals)
python "...skills\domain-intel\scripts\domain_intel.py" available coolstartup.io

# Bulk analysis — multiple domains, multiple checks in parallel
python "...skills\domain-intel\scripts\domain_intel.py" bulk example.com github.com google.com
python "...skills\domain-intel\scripts\domain_intel.py" bulk example.com github.com --checks ssl,dns
```

All output is structured JSON.

## Available Commands

| Command      | What it does                              | Data source                       |
|--------------|-------------------------------------------|-----------------------------------|
| `subdomains` | Find subdomains from certificate logs     | crt.sh (HTTPS)                    |
| `ssl`        | Inspect TLS certificate details           | Direct TCP:443 to target          |
| `whois`      | Registration info, registrar, dates       | WHOIS servers (TCP:43)            |
| `dns`        | A, AAAA, MX, NS, TXT, CNAME records      | System DNS + Google DoH           |
| `available`  | Check if domain is registered             | DNS + WHOIS + SSL signals         |
| `bulk`       | Run multiple checks on multiple domains   | All of the above                  |

## When to Use This vs Other Tools

| Task                              | Better Tool            | Why                                      |
|-----------------------------------|------------------------|------------------------------------------|
| "Что делает этот сайт?"           | `firecrawl scrape`     | Нужен контент страницы, не DNS/WHOIS     |
| "Найди инфо о компании"           | `firecrawl search`     | Общий поиск, не инфраструктура домена    |
| "Поддомены X"                     | **domain-intel**       | Единственный пассивный источник          |
| "SSL сертификат истекает когда?"  | **domain-intel**       | Встроенные инструменты не проверяют TLS  |
| "Кто зарегистрировал домен?"      | **domain-intel**       | WHOIS данные                             |
| "Доступен ли coolstartup.io?"     | **domain-intel**       | Пассивная проверка DNS+WHOIS+SSL         |

## Platform Compatibility

Pure Python stdlib (`socket`, `ssl`, `urllib`, `json`, `concurrent.futures`).

- **crt.sh queries** — HTTPS (port 443), works behind most firewalls
- **WHOIS queries** — TCP port 43 — may be blocked on restrictive networks
- **DNS queries** — Google DoH (HTTPS) for MX/NS/TXT — firewall-friendly
- **SSL checks** — TCP:443 to target — only "active" operation

## Data Sources (All Passive)

- **crt.sh** — Certificate Transparency logs (subdomain discovery)
- **WHOIS servers** — Direct TCP to 100+ authoritative TLD registrars
- **Google DNS-over-HTTPS** — MX, NS, TXT, CNAME resolution
- **System DNS** — A/AAAA record resolution
- **SSL check** — only active operation (TCP to target:443)

## Pitfalls

- WHOIS queries use TCP:43 — may be blocked on restrictive networks
- Some WHOIS servers redact registrant info (GDPR) — notify user
- crt.sh can be slow for very popular domains (thousands of certs)
- Availability check is heuristic-based (3 passive signals) — not authoritative like registrar API
- On Windows: use `python` not `python3`

## Integration with INTEL-SIGHT

This skill directly feeds into INTEL-SIGHT case investigations:
1. Run `subdomains` + `dns` to map corporate infrastructure
2. Run `whois` to identify registrant and registration timeline
3. Run `ssl` to verify certificate legitimacy and SANs
4. Export JSON → feed into `PROJECT/INTEL-SIGHT/` case files

---
*Ported from NousResearch/hermes-agent by Antigravity NEXUS. Original contributor: [@FurkanL0](https://github.com/FurkanL0)*
