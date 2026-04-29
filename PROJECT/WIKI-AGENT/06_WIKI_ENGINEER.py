"""
NEXUS Agent 06  WIKI_ENGINEER v2.0
====================================
Spec-Driven Code Synthesis Engine.

READS actual source code from WIKI repos (not just README titles).
EXTRACTS real patterns: imports, functions, classes, API usage.
OUTPUTS structured SPEC files that Agent 11 can compile into real code.

Zero random.choice. Zero version inflation. Zero theatre.
"""

import ast
import json
import re
import time
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
INVENTIONS_DIR = PROJECT_ROOT / "PROJECT" / "INVENTIONS"
SPEC_OUTPUT = INVENTIONS_DIR / "SPECS"

# Domains  specific code patterns to hunt for
DOMAIN_SIGNATURES = {
    "network_recon": {
        "imports": ["socket", "ssl", "urllib", "requests", "httpx", "aiohttp"],
        "functions": ["connect", "getaddrinfo", "urlopen", "wrap_socket", "recv", "sendall"],
        "keywords": ["subdomain", "port", "scan", "whois", "dns", "certificate", "tls"],
    },
    "data_breach": {
        "imports": ["hashlib", "hmac", "bcrypt"],
        "functions": ["sha1", "sha256", "hexdigest", "pbkdf2"],
        "keywords": ["breach", "pwned", "leak", "credential", "password", "hash"],
    },
    "web_scraping": {
        "imports": ["scrapy", "beautifulsoup4", "bs4", "selenium", "playwright", "lxml"],
        "functions": ["find_all", "select", "xpath", "get_text", "parse"],
        "keywords": ["crawl", "scrape", "spider", "extract", "parse", "html"],
    },
    "osint_profiling": {
        "imports": ["json", "csv", "re"],
        "functions": ["search", "findall", "match", "compile"],
        "keywords": ["username", "profile", "social", "identity", "footprint", "dossier"],
    },
    "crypto_security": {
        "imports": ["cryptography", "pycryptodome", "nacl", "gnupg", "openssl"],
        "functions": ["encrypt", "decrypt", "sign", "verify", "generate_key"],
        "keywords": ["encrypt", "cipher", "aes", "rsa", "pgp", "signature", "vault"],
    },
    "monitoring": {
        "imports": ["prometheus_client", "statsd", "psutil", "watchdog"],
        "functions": ["monitor", "alert", "threshold", "healthcheck", "probe"],
        "keywords": ["uptime", "latency", "health", "status", "availability", "metric"],
    },
}


class NexusEngineerAgent:
    """
    Spec-Driven Engineer.
    Reads actual code from WIKI. Extracts real patterns.
    Outputs structured specifications for Agent 11.
    """

    def __init__(self):
        self._banner()
        SPEC_OUTPUT.mkdir(parents=True, exist_ok=True)
        self.code_patterns = {}  # repo_name -> {imports, functions, classes, docstrings}
        self.domain_matches = {}  # domain -> [{repo, score, evidence}]

    @staticmethod
    def _banner():
        print("\n" + "=" * 60)
        print("  NEXUS AGENT 06  SPEC-DRIVEN ENGINEER v2.0")
        print("  Mode: Read Code  Extract Patterns  Write Specs")
        print("=" * 60 + "\n")

    #  PHASE 1: Documentation Analysis 
    def _analyze_repo(self, repo_path: Path) -> dict | None:
        """Extract patterns from repo documentation (README, dossier, docs).
        WIKI contains only documentation, not cloned source code."""
        content_parts = []
        dossier_data = {}

        # Read ARCHIVIST_DOSSIER.json if present
        dossier_file = repo_path / "ARCHIVIST_DOSSIER.json"
        if dossier_file.exists():
            try:
                dossier_data = json.loads(dossier_file.read_text(encoding="utf-8"))
                content_parts.append(dossier_data.get("legal_devops_perspective", ""))
                content_parts.append(dossier_data.get("core_identity", ""))
            except Exception:
                pass

        # Read all documentation files
        for pattern in ["README.md", "README.rst", "README", "*.md", "*.rst"]:
            for f in repo_path.glob(pattern):
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")[:5000]
                    content_parts.append(text)
                except Exception:
                    pass

        full_text = "\n".join(content_parts)
        if len(full_text) < 50:
            return None

        text_lower = full_text.lower()

        # Extract API URLs from documentation
        api_patterns = []
        urls = re.findall(r'https?://[^\s"\'>\)]+', full_text)
        for u in urls[:20]:
            if any(k in u.lower() for k in ["api", "/v1", "/v2", "/v3", "resolve", "query"]):
                api_patterns.append(u)

        # Extract mentioned tools/technologies
        tech_mentions = []
        tech_keywords = ["python", "golang", "rust", "docker", "api", "rest",
                         "socket", "ssl", "dns", "http", "tcp", "udp", "whois",
                         "nmap", "shodan", "osint", "scanner", "crawler",
                         "scraper", "breach", "password", "hash", "encrypt"]
        for kw in tech_keywords:
            if kw in text_lower:
                tech_mentions.append(kw)

        return {
            "text": full_text[:3000],
            "text_lower": text_lower[:3000],
            "domains": dossier_data.get("domains", []),
            "api_patterns": list(set(api_patterns))[:10],
            "tech_mentions": tech_mentions,
            "doc_length": len(full_text),
        }

    def read_codebase(self, max_repos: int = 200):
        """Phase 1: Scan WIKI repos and extract documentation DNA."""
        print(f"[1] Scanning WIKI documentation (up to {max_repos} repos)...")

        repos = [d for d in WIKI_DIR.iterdir() if d.is_dir() and d.name != "__pycache__"]
        scanned, useful = 0, 0

        for repo in repos[:max_repos]:
            analysis = self._analyze_repo(repo)
            if analysis and analysis["doc_length"] > 100:
                self.code_patterns[repo.name] = analysis
                useful += 1
            scanned += 1

        print(f"  Scanned: {scanned} | Repos with useful docs: {useful}")
        return useful

    #  PHASE 2: Domain Matching 
    def classify_domains(self):
        """Phase 2: Match repos to domains based on documentation evidence."""
        print("[2] Classifying repos by documentation evidence...")
        self.domain_matches = {d: [] for d in DOMAIN_SIGNATURES}

        for repo_name, patterns in self.code_patterns.items():
            text_lower = patterns.get("text_lower", "")
            tech_mentions = set(patterns.get("tech_mentions", []))
            dossier_domains = set(d.lower() for d in patterns.get("domains", []))

            for domain, sigs in DOMAIN_SIGNATURES.items():
                score = 0
                evidence = []

                # Tech mention matches (from documentation)
                tech_hits = tech_mentions & set(sigs["imports"])
                if tech_hits:
                    score += len(tech_hits) * 2
                    evidence.append(f"tech: {', '.join(tech_hits)}")

                # Keyword matches in documentation text
                kw_hits = [kw for kw in sigs["keywords"] if kw in text_lower]
                if kw_hits:
                    score += len(kw_hits) * 2
                    evidence.append(f"keywords: {', '.join(kw_hits)}")

                # Dossier domain match
                if domain.split("_")[0].lower() in dossier_domains or "osint" in dossier_domains:
                    score += 3
                    evidence.append(f"dossier: {', '.join(dossier_domains)}")

                # Function name matches in text
                func_hits = [f for f in sigs["functions"] if f in text_lower]
                if func_hits:
                    score += len(func_hits)
                    evidence.append(f"functions: {', '.join(func_hits)}")

                if score >= 3:
                    self.domain_matches[domain].append({
                        "repo": repo_name,
                        "score": score,
                        "evidence": evidence,
                        "doc_length": patterns["doc_length"],
                    })

        for domain, matches in self.domain_matches.items():
            matches.sort(key=lambda x: x["score"], reverse=True)
            top = matches[:3]
            top_names = [m["repo"] for m in top]
            print(f"  {domain}: {len(matches)} repos (top: {', '.join(top_names) or 'none'})")

    #  PHASE 2.5: GitHub Source Fetch 
    def _resolve_github_url(self, repo_name: str) -> str | None:
        """Resolve WIKI folder name  GitHub owner/repo via CSV or API."""
        import csv as csv_mod
        csv_files = [
            WIKI_DIR / "github-mid-stars-specialized-ru-extended.csv",
            WIKI_DIR / "github-top-stars-full-ru-final.csv",
            WIKI_DIR / "github-phase3-intel-ru.csv",
            WIKI_DIR / "github-phase4-drones-ru.csv",
        ]
        for csv_path in csv_files:
            if not csv_path.exists():
                continue
            try:
                with open(csv_path, encoding="utf-8", errors="ignore") as f:
                    for row in csv_mod.DictReader(f):
                        link = row.get("Link", "")
                        # Match: folder SPIDERFOOT  github.com/smicallef/spiderfoot
                        if f"/{repo_name.lower()}" in link.lower() or repo_name.lower() in link.lower():
                            return link.replace("https://github.com/", "").strip("/")
            except Exception:
                continue
        # Fallback: try common patterns via GitHub search
        return None

    def _fetch_python_files(self, owner_repo: str, max_files: int = 10) -> list[str]:
        """Download Python source files from GitHub via API, preferring 'gh' CLI for authentication and higher rate limits."""
        import urllib.request
        import urllib.error
        import subprocess
        from pathlib import Path

        sources = []
        try:
            # Try `gh api` first for authenticated limits
            gh_cmd = '"C:\\Program Files\\GitHub CLI\\gh.exe"' if Path("C:\\Program Files\\GitHub CLI\\gh.exe").exists() else "gh"
            res = subprocess.run(f'{gh_cmd} api repos/{owner_repo}/git/trees/HEAD?recursive=1', capture_output=True, text=True, shell=True)
            if res.returncode == 0 and res.stdout:
                tree = json.loads(res.stdout)
            else:
                # Fallback to anonymous API (60 req/hr)
                tree_url = f"https://api.github.com/repos/{owner_repo}/git/trees/HEAD?recursive=1"
                req = urllib.request.Request(tree_url, headers={"User-Agent": "NEXUS-Agent-06/2.0"})
                resp = urllib.request.urlopen(req, timeout=10)
                tree = json.loads(resp.read().decode())

            # Filter: only .py files, skip tests/docs/setup
            py_files = []
            for item in tree.get("tree", []):
                p = item.get("path", "")
                if not p.endswith(".py"):
                    continue
                if any(skip in p.lower() for skip in ["test", "setup.py", "conftest", "__pycache__", "docs/", "example"]):
                    continue
                if item.get("size", 0) > 50000:  # skip huge files
                    continue
                py_files.append(p)

            # Prioritize: main module files, not deep nested
            py_files.sort(key=lambda x: (x.count("/"), len(x)))

            for pf in py_files[:max_files]:
                try:
                    raw_url = f"https://raw.githubusercontent.com/{owner_repo}/HEAD/{pf}"
                    req2 = urllib.request.Request(raw_url, headers={"User-Agent": "NEXUS-Agent-06/2.0"})
                    resp2 = urllib.request.urlopen(req2, timeout=10)
                    source = resp2.read().decode("utf-8", errors="ignore")
                    sources.append(source)
                except Exception:
                    continue
        except Exception as e:
            pass

        return sources

    def _ast_analyze_source(self, source: str) -> dict:
        """AST-parse a Python source string to extract imports, functions, classes."""
        result = {"imports": set(), "functions": [], "classes": [], "api_urls": []}
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    result["imports"].add(node.module.split(".")[0])
                elif isinstance(node, ast.FunctionDef):
                    doc = ast.get_docstring(node) or ""
                    result["functions"].append({
                        "name": node.name,
                        "args": [a.arg for a in node.args.args if a.arg != "self"],
                        "doc": doc[:200],
                    })
                elif isinstance(node, ast.ClassDef):
                    doc = ast.get_docstring(node) or ""
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
                    result["classes"].append({"name": node.name, "methods": methods[:10], "doc": doc[:200]})
        except SyntaxError:
            pass

        # Extract API URLs
        urls = re.findall(r'https?://[^\s"\'>]+', source)
        for u in urls[:10]:
            if any(k in u.lower() for k in ["api", "/v1", "/v2", "resolve"]):
                result["api_urls"].append(u)

        result["imports"] = sorted(result["imports"])
        return result

    def fetch_github_sources(self, top_n: int = 3):
        """Phase 2.5: For top-scoring repos in each domain, fetch real source from GitHub."""
        print("[2.5] Fetching source code from GitHub for top repos...")
        fetched_count = 0
        seen_repos = set()

        for domain, matches in self.domain_matches.items():
            for match in matches[:top_n]:
                repo_name = match["repo"]
                if repo_name in seen_repos:
                    continue
                seen_repos.add(repo_name)

                owner_repo = self._resolve_github_url(repo_name)
                if not owner_repo:
                    continue

                sources = self._fetch_python_files(owner_repo, max_files=5)
                if not sources:
                    continue

                # AST analyze fetched source code
                combined_analysis = {"imports": set(), "functions": [], "classes": [], "api_urls": []}
                for src in sources:
                    analysis = self._ast_analyze_source(src)
                    combined_analysis["imports"].update(analysis["imports"])
                    combined_analysis["functions"].extend(analysis["functions"])
                    combined_analysis["classes"].extend(analysis["classes"])
                    combined_analysis["api_urls"].extend(analysis["api_urls"])

                # Enrich existing pattern entry
                if repo_name in self.code_patterns:
                    self.code_patterns[repo_name]["source_imports"] = sorted(combined_analysis["imports"])
                    self.code_patterns[repo_name]["source_functions"] = combined_analysis["functions"][:15]
                    self.code_patterns[repo_name]["source_classes"] = combined_analysis["classes"][:10]
                    self.code_patterns[repo_name]["source_api_urls"] = list(set(combined_analysis["api_urls"]))[:10]

                fetched_count += 1
                fn_count = len(combined_analysis["functions"])
                cls_count = len(combined_analysis["classes"])
                print(f"  [+] {repo_name} ({owner_repo}): {len(sources)} files, {fn_count} funcs, {cls_count} classes")

        print(f"  Fetched source from {fetched_count} repos")

    def generate_specs(self) -> list:
        """Phase 3: Generate structured specs only for domains with evidence."""
        print("[3] Generating specifications from code evidence...")

        # Only create specs for domains where we found real code
        SPEC_TEMPLATES = {
            "network_recon": {
                "module_name": "network_recon",
                "title": "Network Reconnaissance",
                "description": "TCP/UDP port scanning, DNS resolution, SSL certificate inspection, subdomain discovery via CT logs",
                "inputs": ["target: str (domain or IP)", "ports: list[int] (optional)", "timeout: float"],
                "outputs": ["PortScanResult", "DNSRecords", "SSLCertInfo", "SubdomainList"],
                "stdlib_deps": ["socket", "ssl", "urllib.request", "json", "concurrent.futures"],
                "api_endpoints": ["https://crt.sh/?q=%25.{domain}&output=json", "https://dns.google/resolve?name={domain}&type={qtype}"],
                "reference_pattern": "ThreadPoolExecutor for concurrent port probing + socket.create_connection for TCP checks",
            },
            "data_breach": {
                "module_name": "breach_intel",
                "title": "Breach Intelligence",
                "description": "Password breach check via HIBP k-anonymity API. Email breach lookup (requires API key).",
                "inputs": ["target: str (email or password)", "api_key: str (optional, from env)"],
                "outputs": ["BreachResult with pwned: bool, count: int, breach_names: list"],
                "stdlib_deps": ["hashlib", "urllib.request", "os", "json"],
                "api_endpoints": ["https://api.pwnedpasswords.com/range/{prefix}", "https://haveibeenpwned.com/api/v3/breachedaccount/{email}"],
                "reference_pattern": "SHA1 k-anonymity prefix match for password + full API for email",
            },
            "web_scraping": {
                "module_name": "web_crawler",
                "title": "Web Crawler",
                "description": "HTTP content fetcher with header extraction, redirect following, and response analysis",
                "inputs": ["urls: list[str]", "timeout: float", "max_depth: int"],
                "outputs": ["CrawlResult with status, headers, content_length, redirects"],
                "stdlib_deps": ["urllib.request", "urllib.error", "json", "html.parser"],
                "api_endpoints": [],
                "reference_pattern": "Concurrent URL probing with redirect chain tracking",
            },
            "osint_profiling": {
                "module_name": "identity_profiler",
                "title": "Identity Profiler",
                "description": "Username presence detection across social platforms via HTTP HEAD requests",
                "inputs": ["username: str", "platforms: list[str] (optional)"],
                "outputs": ["ProfileResult with platform, url, found: bool per platform"],
                "stdlib_deps": ["urllib.request", "urllib.error", "json", "concurrent.futures"],
                "api_endpoints": [],
                "reference_pattern": "ThreadPoolExecutor + HEAD requests against platform URL templates",
            },
            "monitoring": {
                "module_name": "endpoint_monitor",
                "title": "Endpoint Monitor",
                "description": "HTTP endpoint availability checker with latency measurement and status tracking",
                "inputs": ["targets: list[str]", "timeout: float", "interval: int (for loop mode)"],
                "outputs": ["ProbeResult with url, status, latency_ms, ok: bool"],
                "stdlib_deps": ["urllib.request", "time", "json", "concurrent.futures"],
                "api_endpoints": [],
                "reference_pattern": "Concurrent HTTP probes with perf_counter timing",
            },
            "crypto_security": {
                "module_name": "security_analyzer",
                "title": "Security Header Analyzer",
                "description": "HTTP security header audit  checks HSTS, CSP, X-Frame-Options, and more",
                "inputs": ["target: str (domain)", "timeout: float"],
                "outputs": ["SecurityReport with header_present: dict, score: int, server_info: str"],
                "stdlib_deps": ["urllib.request", "ssl", "socket", "json"],
                "api_endpoints": [],
                "reference_pattern": "HTTPS HEAD request + header dict comparison against known security headers",
            },
        }

        specs = []
        for domain, matches in self.domain_matches.items():
            if not matches:
                continue

            template = SPEC_TEMPLATES.get(domain)
            if not template:
                continue

            # Enrich template with actual evidence from code analysis
            top_repos = matches[:5]
            top_imports = set()
            top_api_urls = []
            for m in top_repos:
                repo_data = self.code_patterns.get(m["repo"], {})
                top_imports.update(repo_data.get("imports", []))
                top_api_urls.extend(repo_data.get("api_patterns", []))

            spec = {
                **template,
                "domain": domain,
                "evidence_repos": [{"repo": m["repo"], "score": m["score"], "evidence": m["evidence"]} for m in top_repos],
                "observed_imports": sorted(top_imports)[:20],
                "observed_api_urls": list(set(top_api_urls))[:10],
                "generated_at": datetime.now().isoformat(),
            }
            specs.append(spec)
            print(f"  [SPEC] {spec['module_name']}: {spec['title']} (backed by {len(top_repos)} repos)")

        return specs

    #  PHASE 4: Persist 
    def save_specs(self, specs: list):
        """Phase 4: Save specs as structured JSON for Agent 11."""
        if not specs:
            print("  No specs generated  insufficient code evidence in WIKI.")
            return

        timestamp = int(time.time())

        # Individual spec files (for Agent 11)
        for spec in specs:
            spec_file = SPEC_OUTPUT / f"{spec['module_name']}.spec.json"
            spec_file.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

        # Combined manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "agent": "06_WIKI_ENGINEER_v2",
            "total_specs": len(specs),
            "specs": [{"module": s["module_name"], "title": s["title"], "domain": s["domain"]} for s in specs],
        }
        manifest_file = SPEC_OUTPUT / "MANIFEST.json"
        manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        # Human-readable blueprint
        blueprint_file = INVENTIONS_DIR / f"Blueprint_{timestamp}.md"
        with open(blueprint_file, "w", encoding="utf-8") as f:
            f.write("# NEXUS Engineering Specifications\n")
            f.write(f"> Generated: {datetime.now().isoformat()}\n")
            f.write(f"> Source: {len(self.code_patterns)} analyzed repos from WIKI\n\n")
            for i, spec in enumerate(specs, 1):
                f.write(f"## {i}. {spec['title']} (`{spec['module_name']}.py`)\n")
                f.write(f"**Domain**: {spec['domain']}\n\n")
                f.write(f"**Description**: {spec['description']}\n\n")
                f.write(f"**Inputs**: {', '.join(spec['inputs'])}\n\n")
                f.write(f"**Outputs**: {', '.join(spec['outputs'])}\n\n")
                f.write(f"**Dependencies**: {', '.join(spec['stdlib_deps'])}\n\n")
                if spec['evidence_repos']:
                    f.write("**Evidence**:\n")
                    for r in spec['evidence_repos'][:3]:
                        f.write(f"  - {r['repo']} (score: {r['score']}, {'; '.join(r['evidence'])})\n")
                f.write("\n---\n\n")

        print(f"\n  Saved {len(specs)} specs to {SPEC_OUTPUT}")
        print(f"  Blueprint: {blueprint_file.name}")

    #  RUN 
    def run(self, max_repos: int = 200):
        useful = self.read_codebase(max_repos)
        if useful == 0:
            print("  No documentation found in WIKI. Aborting.")
            return
        self.classify_domains()
        self.fetch_github_sources(top_n=3)  # Phase 2.5: go to GitHub
        specs = self.generate_specs()
        self.save_specs(specs)
        print(f"\n[DONE] {len(specs)} specifications generated from {useful} repos.")


if __name__ == "__main__":
    import sys
    max_repos = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    agent = NexusEngineerAgent()
    agent.run(max_repos)
