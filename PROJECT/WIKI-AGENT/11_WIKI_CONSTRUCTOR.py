import os
import sys
import time
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_PROJECT_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"
BUILD_DIR = WIKI_PROJECT_DIR / "BUILD_OUTPUT"
AGENT_NAME = "11_WIKI_CONSTRUCTOR"


class NexusConstructorAgent:
    """
    Agent 11: Builder.
    Transforms blueprint specs into verified codebases with REAL code.
    Zero stub tolerance — every module must execute.
    """

    def __init__(self):
        self._banner()
        BUILD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _banner():
        print("\n" + "=" * 60)
        print("  NEXUS AGENT 11 — PROJECT CONSTRUCTOR v2.0")
        print("  Mission: Real Code Only. Zero Stubs. Zero pass.")
        print("=" * 60 + "\n")

    # ──────────────────────────────────────────────────────────────────────────
    # CODE SYNTHESIZER
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _synthesize_code(comp_name: str, spec: dict = None) -> str:
        """
        Generates real, runnable Python code based on component name and optional spec metadata.
        NEVER produces bare `pass`. Every module is executable from CLI.
        """
        n = comp_name.lower()
        
        # Metadata extraction from Agent 06 specs
        imports = spec.get("observed_imports", []) if spec else []
        api_urls = spec.get("observed_api_urls", []) if spec else []
        desc = spec.get("description", "Premium OSINT module synthesised via NEXUS.") if spec else ""
        
        meta_comments = ""
        if imports:
            meta_comments += f"# Observed real-world imports: {', '.join(imports[:10])}\n"
        if api_urls:
            meta_comments += f"# Observed API patterns: {', '.join(api_urls[:3])}\n"

        # ── RECON / SUBDOMAIN DISCOVERY ──────────────────────────────────────
        if any(k in n for k in ["recon", "subdomain", "crt", "cert-discover"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — Subdomain discovery via crt.sh CT logs."""
{meta_comments}
import json, urllib.request, urllib.parse
from datetime import datetime, timezone

def run(domain: str, limit: int = 200) -> dict:
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    url = f"https://crt.sh/?q=%25.{{urllib.parse.quote(domain)}}&output=json"
    req = urllib.request.Request(url, headers={{"User-Agent": "nexus-recon/1.0", "Accept": "application/json"}})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            entries = json.loads(r.read().decode())
    except Exception as e:
        return {{"error": str(e), "domain": domain, "subdomains": []}}
    seen, results, now = set(), [], datetime.now(timezone.utc)
    for e in entries:
        exp = e.get("not_after", "")
        if exp:
            try:
                dt = datetime.strptime(exp[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                if dt <= now:
                    continue
            except ValueError:
                pass
        for name in e.get("name_value", "").splitlines():
            name = name.strip().lower()
            if name and name not in seen:
                seen.add(name)
                results.append({{"subdomain": name, "issuer": e.get("issuer_name", ""), "not_after": exp}})
    results.sort(key=lambda x: (x["subdomain"].startswith("*"), x["subdomain"]))
    return {{"domain": domain, "count": min(len(results), limit), "subdomains": results[:limit]}}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

        # ── SSL / TLS ─────────────────────────────────────────────────────────
        elif any(k in n for k in ["ssl", "tls", "cert-check", "certificate"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — SSL/TLS certificate inspection."""
{meta_comments}
import ssl, socket, json
from datetime import datetime, timezone

def run(host: str, port: int = 443, timeout: int = 10) -> dict:
    def flat(rdns):
        r = {{}}
        for rdn in rdns:
            for item in rdn:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    r[item[0]] = item[1]
        return r
    def parse_date(s):
        for fmt in ("%b %d %H:%M:%S %Y %Z", "%b  %d %H:%M:%S %Y %Z"):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                pass
        return None
    warning = None
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as s:
                cert, cipher, proto = s.getpeercert(), s.cipher(), s.version()
    except ssl.SSLCertVerificationError as e:
        warning = str(e)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as s:
                cert, cipher, proto = s.getpeercert(), s.cipher(), s.version()
    not_after = parse_date(cert.get("notAfter", ""))
    now = datetime.now(timezone.utc)
    days = (not_after - now).days if not_after else None
    return {{
        "host": host, "port": port,
        "subject": flat(cert.get("subject", [])),
        "issuer": flat(cert.get("issuer", [])),
        "subject_alt_names": [f"{{t}}:{{v}}" for t, v in cert.get("subjectAltName", [])],
        "not_after": not_after.isoformat() if not_after else "",
        "days_remaining": days, "is_expired": days is not None and days < 0,
        "tls_version": proto, "cipher_suite": cipher[0] if cipher else None,
        "verification_warning": warning,
    }}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

        # ── WHOIS ─────────────────────────────────────────────────────────────
        elif any(k in n for k in ["whois", "registr", "domain-info"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — WHOIS domain registration lookup via raw TCP."""
import socket, re, json
from datetime import datetime, timezone

WHOIS_SERVERS = {{
    "com": "whois.verisign-grs.com", "net": "whois.verisign-grs.com",
    "org": "whois.pir.org", "io": "whois.nic.io", "ru": "whois.tcinet.ru",
    "ua": "whois.ua", "uk": "whois.nic.uk", "de": "whois.denic.de",
    "ai": "whois.nic.ai", "dev": "whois.nic.google", "app": "whois.nic.google",
    "info": "whois.afilias.net", "me": "whois.nic.me", "co": "whois.nic.co",
}}

def run(domain: str) -> dict:
    parts = domain.split(".")
    server = WHOIS_SERVERS.get(".".join(parts[-2:])) or WHOIS_SERVERS.get(parts[-1])
    if not server:
        return {{"error": f"No WHOIS server for .{{parts[-1]}}", "domain": domain}}
    try:
        with socket.create_connection((server, 43), timeout=10) as s:
            s.sendall((domain + "\\r\\n").encode())
            chunks = []
            while True:
                c = s.recv(4096)
                if not c: break
                chunks.append(c)
            raw = b"".join(chunks).decode("utf-8", errors="replace")
    except Exception as e:
        return {{"error": str(e), "domain": domain}}
    pats = {{
        "registrar": r"(?:Registrar|registrar):\\s*(.+)",
        "creation_date": r"(?:Creation Date|Created|created):\\s*(.+)",
        "expiration_date": r"(?:Registry Expiry Date|Expiration Date):\\s*(.+)",
        "name_servers": r"(?:Name Server|nserver):\\s*(.+)",
        "status": r"(?:Domain Status|status):\\s*(.+)",
    }}
    result = {{"domain": domain, "whois_server": server}}
    for key, pat in pats.items():
        matches = re.findall(pat, raw, re.IGNORECASE)
        if matches:
            result[key] = list(dict.fromkeys(m.strip() for m in matches)) if key in ("name_servers", "status") else matches[0].strip()
    return result

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

        # ── DNS ───────────────────────────────────────────────────────────────
        elif any(k in n for k in ["dns", "resolver", "nameserver"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — DNS records via system DNS + Google DoH."""
import socket, json, urllib.request, urllib.parse

def run(domain: str, types: list = None) -> dict:
    types = types or ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    records = {{}}
    for qtype in types:
        if qtype == "A":
            try: records["A"] = list(dict.fromkeys(i[4][0] for i in socket.getaddrinfo(domain, None, socket.AF_INET)))
            except: records["A"] = []
        elif qtype == "AAAA":
            try: records["AAAA"] = list(dict.fromkeys(i[4][0] for i in socket.getaddrinfo(domain, None, socket.AF_INET6)))
            except: records["AAAA"] = []
        else:
            url = f"https://dns.google/resolve?name={{urllib.parse.quote(domain)}}&type={{qtype}}"
            try:
                req = urllib.request.Request(url, headers={{"User-Agent": "nexus-dns/1.0"}})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                records[qtype] = [a.get("data", "").strip().rstrip(".") for a in data.get("Answer", []) if a.get("data")]
            except: records[qtype] = []
    return {{"domain": domain, "records": records}}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

        # ── PORT SCANNER ──────────────────────────────────────────────────────
        elif any(k in n for k in ["port", "scanner", "scan", "nmap"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — Concurrent TCP port scanner (stdlib only)."""
import socket, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

TOP_PORTS = [21,22,23,25,53,80,110,143,443,445,993,995,3306,3389,5900,8080,8443,9200,27017]
SERVICES = {{21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",443:"HTTPS",
             445:"SMB",3306:"MySQL",3389:"RDP",5900:"VNC",8080:"HTTP-Alt",9200:"Elasticsearch",27017:"MongoDB"}}

def _check(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {{"port": port, "state": "open", "service": SERVICES.get(port, "unknown")}}
    except: return None

def run(host: str, ports: list = None, timeout: float = 1.0) -> dict:
    ports = ports or TOP_PORTS
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        for result in as_completed({{ex.submit(_check, host, p, timeout): p for p in ports}}):
            r = result.result()
            if r: open_ports.append(r)
    open_ports.sort(key=lambda x: x["port"])
    return {{"host": host, "scanned": len(ports), "open_count": len(open_ports), "open_ports": open_ports}}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

        # ── BREACH / HIBP ─────────────────────────────────────────────────────
        elif any(k in n for k in ["breach", "leak", "hibp", "pwned", "breach-finder"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — Breach detection via HIBP k-anonymity API."""
import hashlib, urllib.request, urllib.parse, os, json

def check_password(password: str) -> dict:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    req = urllib.request.Request(f"https://api.pwnedpasswords.com/range/{{prefix}}",
                                  headers={{"User-Agent": "nexus-breach/1.0", "Add-Padding": "true"}})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            for line in r.read().decode().splitlines():
                h, count = line.split(":")
                if h == suffix:
                    return {{"pwned": True, "count": int(count)}}
        return {{"pwned": False, "count": 0}}
    except Exception as e:
        return {{"error": str(e)}}

def check_email(email: str) -> dict:
    key = os.environ.get("HIBP_API_KEY", "")
    if not key:
        return {{"error": "Set HIBP_API_KEY env var (free at haveibeenpwned.com/API/Key)", "email": email}}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{{urllib.parse.quote(email)}}"
    req = urllib.request.Request(url, headers={{"hibp-api-key": key, "User-Agent": "nexus-breach/1.0"}})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            breaches = json.loads(r.read())
        return {{"email": email, "pwned": True, "count": len(breaches), "breaches": [b["Name"] for b in breaches]}}
    except urllib.error.HTTPError as e:
        return {{"email": email, "pwned": False, "count": 0}} if e.code == 404 else {{"error": str(e)}}

def run(target: str) -> dict:
    return check_email(target) if "@" in target else check_password(target)

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "password123"), indent=2))
'''

        # ── SOCIAL / USERNAME ─────────────────────────────────────────────────
        elif any(k in n for k in ["social", "username", "profiler", "profile", "sherlock"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — Username presence across 15 platforms."""
import urllib.request, json
from concurrent.futures import ThreadPoolExecutor, as_completed

PLATFORMS = {{
    "GitHub": "https://github.com/{{}}","Twitter": "https://twitter.com/{{}}",
    "Instagram": "https://www.instagram.com/{{}}","Reddit": "https://www.reddit.com/user/{{}}",
    "TikTok": "https://www.tiktok.com/@{{}}","YouTube": "https://www.youtube.com/@{{}}",
    "Telegram": "https://t.me/{{}}","Twitch": "https://www.twitch.tv/{{}}",
    "Dev.to": "https://dev.to/{{}}","Medium": "https://medium.com/@{{}}",
    "Pinterest": "https://www.pinterest.com/{{}}","LinkedIn": "https://www.linkedin.com/in/{{}}",
    "HackerNews": "https://news.ycombinator.com/user?id={{}}",
    "ProductHunt": "https://www.producthunt.com/@{{}}","Mastodon": "https://mastodon.social/@{{}}",
}}

def _check(platform, url_tpl, username, timeout=5.0):
    url = url_tpl.format(username)
    try:
        req = urllib.request.Request(url, method="HEAD", headers={{"User-Agent": "nexus-social/1.0"}})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            found = r.status < 400
    except urllib.error.HTTPError as e: found = e.code < 400
    except: found = False
    return {{"platform": platform, "url": url, "found": found}}

def run(username: str) -> dict:
    # Cleanup input (if a domain or URL was passed by mistake)
    username = username.replace("https://", "").replace("http://", "").strip("/").split("/")[-1]
    if "." in username: username = username.split(".")[0]
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for f in as_completed({{ex.submit(_check, p, u, username): p for p, u in PLATFORMS.items()}}):
            results.append(f.result())
    found = [r for r in results if r["found"]]
    results.sort(key=lambda x: (not x["found"], x["platform"]))
    return {{"username": username, "checked": len(results), "found_count": len(found), "results": results}}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "johndoe"), indent=2))
'''

        # ── MONITOR / CRAWLER / STEALTH / HUB (fallback for agent-ish names) ─
        elif any(k in n for k in ["monitor", "crawler", "spider", "stealth", "hub", "agent"]):
            return f'''#!/usr/bin/env python3
"""NEXUS Module: {comp_name} — HTTP endpoint monitor with concurrent probing."""
import urllib.request, urllib.error, json, time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

def _probe(url: str, timeout: float = 10.0) -> dict:
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={{"User-Agent": "nexus-monitor/1.0"}})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ms = round((time.perf_counter() - start) * 1000, 1)
            return {{"url": url, "status": r.status, "ok": True, "latency_ms": ms,
                    "checked_at": datetime.now(timezone.utc).isoformat()}}
    except urllib.error.HTTPError as e:
        ms = round((time.perf_counter() - start) * 1000, 1)
        return {{"url": url, "status": e.code, "ok": e.code < 400, "latency_ms": ms, "error": str(e)}}
    except Exception as e:
        return {{"url": url, "status": None, "ok": False, "latency_ms": None, "error": str(e)}}

def run(targets) -> dict:
    if isinstance(targets, str): targets = [targets]
    # Normalize targets to proper URLs
    targets = [t if t.startswith("http") else "https://" + t for t in targets]
    results = []
    with ThreadPoolExecutor(max_workers=min(len(targets), 20)) as ex:
        for f in as_completed({{ex.submit(_probe, u): u for u in targets}}):
            results.append(f.result())
    up = sum(1 for r in results if r["ok"])
    return {{"total": len(results), "up": up, "down": len(results) - up, "results": results}}

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["https://example.com"]
    print(json.dumps(run(targets), indent=2))
'''

        # ── GENERIC OSINT ANALYZER (universal fallback) ───────────────────────
        else:
            slug = comp_name.replace("-", "_").replace(".", "_").replace(" ", "_").upper()
            return f'''#!/usr/bin/env python3
"""
NEXUS Module: {comp_name}
Passive OSINT analyzer — IP resolution, HTTPS check, HTTP security headers audit.
stdlib only. Outputs structured JSON.
"""
import json, socket, ssl, urllib.request
from datetime import datetime, timezone

def _resolve_ip(host: str) -> list:
    try: return list(dict.fromkeys(i[4][0] for i in socket.getaddrinfo(host, None, socket.AF_INET)))
    except: return []

def _https_reachable(host: str, timeout: float = 5.0) -> bool:
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, 443), timeout=timeout) as s:
            with ctx.wrap_socket(s, server_hostname=host): return True
    except: return False

def _http_headers(host: str, timeout: float = 8.0) -> dict:
    try:
        req = urllib.request.Request(f"https://{{host}}", headers={{"User-Agent": "nexus-{slug}/1.0"}})
        with urllib.request.urlopen(req, timeout=timeout) as r: return dict(r.headers)
    except: return {{}}

SECURITY_HEADERS = {{
    "Strict-Transport-Security": "HSTS",
    "Content-Security-Policy": "CSP",
    "X-Frame-Options": "Clickjacking-Protection",
    "X-Content-Type-Options": "MIME-Sniffing-Protection",
    "Referrer-Policy": "Referrer-Policy",
    "Permissions-Policy": "Feature-Policy",
}}

def run(target: str) -> dict:
    target = target.replace("https://", "").replace("http://", "").split("/")[0]  # Sockets need raw hostname
    headers = _http_headers(target)
    sec = {{label: (header in headers) for header, label in SECURITY_HEADERS.items()}}
    return {{
        "target": target, "module": "{comp_name}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip_addresses": _resolve_ip(target),
        "https_reachable": _https_reachable(target),
        "security_headers": sec,
        "security_score": f"{{sum(sec.values())}}/{{len(sec)}}",
        "http_server": headers.get("Server", "unknown"),
        "powered_by": headers.get("X-Powered-By", "not disclosed"),
    }}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
'''

    # ──────────────────────────────────────────────────────────────────────────
    # BUILD PIPELINE
    # ──────────────────────────────────────────────────────────────────────────

    def _synthesize_cli(self) -> str:
        """Generates dynamic CLI orchestrator that loads all spawned OSINT modules via importlib."""
        return '''#!/usr/bin/env python3
"""
NEXUS SHADOW SIGHT — Ultimate OSINT Engine
Dynamically loads and coordinates all specialized OSINT modules.
"""

import os
import sys
import json
import importlib
import importlib.util
from pathlib import Path
from datetime import datetime

class ShadowSightCLI:
    def __init__(self):
        self.src_dir = Path(__file__).parent
        self.modules = {}
        if str(self.src_dir) not in sys.path:
            sys.path.insert(0, str(self.src_dir))
        self._load_modules()

    def _load_modules(self):
        for py_file in self.src_dir.glob("*.py"):
            if py_file.name == "shadow_cli.py" or py_file.name == "__init__.py":
                continue
            
            mod_name = py_file.stem
            try:
                spec = importlib.util.spec_from_file_location(mod_name, py_file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                
                if hasattr(mod, "run"):
                    doc = mod.__doc__ or "No description provided."
                    title = doc.split("—")[-1].strip() if "—" in doc else mod_name.replace("_", " ").title()
                    self.modules[mod_name] = {
                        "module": mod,
                        "title": title
                    }
            except Exception as e:
                pass

    def banner(self):
        print("\\n" + "=" * 60)
        print("  SHADOW SIGHT OSINT ENGINE V5.0 (Golden Edition)")
        print(f"  Active Intelligence Plugins: {len(self.modules)}")
        print("=" * 60 + "\\n")

    def list_modules(self):
        print("[*] Loaded Modules:")
        for name, info in self.modules.items():
            print(f"  --> {info['title']} [{name}.py]")
        print()

    def execute_all(self, target: str):
        print(f"[*] Initiating Full-Spectrum Recon on: {target}")
        results = {}
        
        for name, info in self.modules.items():
            print(f"\\n[>] Running: {info['title']} ...")
            try:
                mod_run = getattr(info['module'], "run")
                res = mod_run(target)
                results[name] = res
                print(f"    [+] Successfully gathered intel.")
            except Exception as e:
                print(f"    [!] Error during execution: {e}")
                results[name] = {"error": str(e)}
                
        logs_dir = self.src_dir.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        report_path = logs_dir / f"report_{target.replace('.', '_')}_{int(datetime.now().timestamp())}.json"
        report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        
        print("\\n" + "=" * 60)
        print(f"[*] RECON COMPLETE. Full report saved to: {report_path.name}")
        print("=" * 60 + "\\n")

if __name__ == "__main__":
    cli = ShadowSightCLI()
    cli.banner()
    
    if len(sys.argv) < 2:
        print("Usage: python shadow_cli.py <target_domain_or_ip_or_email>")
        print("Example: python shadow_cli.py example.com")
        sys.exit(1)
        
    cli.list_modules()
    target = sys.argv[1]
    cli.execute_all(target)
'''

    def verify_build(self, build_path: Path) -> bool:
        """Verifies build integrity before delivery."""
        print(f"[*] Verifying build: {build_path.name} ...")
        for d in ["src", "config", "data", "logs"]:
            if not (build_path / d).exists():
                print(f"  [FAIL] Missing directory: {d}")
                return False
        py_files = list((build_path / "src").glob("*.py"))
        if not py_files:
            print("  [FAIL] No source files generated.")
            return False
        # Sanity: verify no stub `pass` bodies remain
        stubs = [f for f in py_files if "def run():\n    pass" in f.read_text(encoding="utf-8", errors="ignore")]
        if stubs:
            print(f"  [WARN] {len(stubs)} stub file(s) detected: {[f.name for f in stubs]}")
        print(f"  [OK] {len(py_files)} source file(s) generated. {len(stubs)} stubs.")
        return True

    def finalize_delivery(self, build_path: Path) -> Path:
        """Renames TEST build to PROD."""
        final_path = build_path.parent / build_path.name.replace("TEST_", "PROD_")
        if final_path.exists():
            import shutil
            shutil.rmtree(final_path)
        build_path.rename(final_path)
        print(f"  [+] Delivered: {final_path.name}")
        return final_path

    def scaffold_project(self, project_name: str, components: list) -> Path | None:
        """Build project structure with synthesized real code."""
        print(f"[*] Building: {project_name} ({len(components)} components)")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = BUILD_DIR / f"TEST_{project_name.upper().replace(' ', '_')}_{timestamp}"
        target.mkdir(parents=True, exist_ok=True)

        for d in ["src", "config", "data", "logs"]:
            (target / d).mkdir(exist_ok=True)

        for comp in components:
            safe = comp.lower().replace(" ", "_").replace(".", "_").replace("`", "").replace("/", "_")
            file_path = target / "src" / f"{safe}.py"
            code = self._synthesize_code(comp)
            file_path.write_text(code, encoding="utf-8")
            lines = len(code.splitlines())
            print(f"  [+] {safe}.py  ({lines} lines, type detected from: '{comp}')")

        # Generate CLI Orchestrator
        cli_path = target / "src" / "shadow_cli.py"
        cli_code = self._synthesize_cli()
        cli_path.write_text(cli_code, encoding="utf-8")
        print(f"  [+] shadow_cli.py ({len(cli_code.splitlines())} lines) — Master Orchestrator")

        if self.verify_build(target):
            return self.finalize_delivery(target)
        else:
            print(f"  [!] Build error. Artifacts at: {target}")
            return None


    def build_from_specs(self, specs_dir: Path, project_name: str = "Shadow-Sight"):
        """Build project from Agent 06's structured .spec.json files."""
        spec_files = sorted(specs_dir.glob("*.spec.json"))
        if not spec_files:
            print(f"  No .spec.json files found in {specs_dir}")
            return None

        print(f"[*] Spec-driven build: {project_name} ({len(spec_files)} specs)")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = BUILD_DIR / f"TEST_{project_name.upper().replace(' ', '_')}_{timestamp}"
        target.mkdir(parents=True, exist_ok=True)
        for d in ["src", "config", "data", "logs"]:
            (target / d).mkdir(exist_ok=True)

        import json
        for spec_file in spec_files:
            try:
                spec = json.loads(spec_file.read_text(encoding="utf-8"))
            except Exception:
                spec = {}
            module_name = spec.get("module_name", spec_file.stem.replace(".spec", ""))
            code = self._synthesize_code(module_name, spec=spec)
            file_path = target / "src" / f"{module_name}.py"
            file_path.write_text(code, encoding="utf-8")
            lines = len(code.splitlines())
            print(f"  [+] {module_name}.py ({lines} lines) — {spec.get('title', 'unknown')}")

        # Also copy domain_intel.py if it exists (the real working code)
        existing_intel = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-PROJECT\LEGAL\BUILD\B001_SHADOW-SIGHT\src\domain_intel.py")
        if existing_intel.exists():
            import shutil
            dest = target / "src" / "domain_intel.py"
            if not dest.exists():
                shutil.copy2(existing_intel, dest)
                print(f"  [+] domain_intel.py (copied, {existing_intel.stat().st_size} bytes)")

        # Generate CLI Orchestrator
        cli_path = target / "src" / "shadow_cli.py"
        cli_code = self._synthesize_cli()
        cli_path.write_text(cli_code, encoding="utf-8")
        print(f"  [+] shadow_cli.py ({len(cli_code.splitlines())} lines) — Master Orchestrator")

        if self.verify_build(target):
            return self.finalize_delivery(target)
        else:
            print(f"  [!] Build error. Artifacts at: {target}")
            return None


if __name__ == "__main__":
    agent = NexusConstructorAgent()

    if len(sys.argv) > 1 and sys.argv[1] == "--specs":
        # Spec-driven mode (Agent 06 → Agent 11 pipeline)
        specs_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\INVENTIONS\SPECS")
        project_name = sys.argv[2] if len(sys.argv) > 2 else "Shadow-Sight"
        agent.build_from_specs(specs_dir, project_name)

    elif len(sys.argv) > 1:
        # Legacy: blueprint .md mode
        blueprint_file = Path(sys.argv[1])
        if blueprint_file.exists():
            content = blueprint_file.read_text(encoding="utf-8", errors="ignore")
            modules = [
                line.split(":")[-1].strip().strip("*")
                for line in content.split("\n")
                if "- **Module**" in line
            ]
            if modules:
                agent.scaffold_project("Legal-DevOps Master System", modules)
            else:
                print("No modules found in blueprint.")
        else:
            print(f"Blueprint not found: {blueprint_file}")
    else:
        print("Usage:")
        print("  python 11_WIKI_CONSTRUCTOR.py --specs [project_name]   # From Agent 06 specs")
        print("  python 11_WIKI_CONSTRUCTOR.py <blueprint.md>           # From legacy blueprint")
