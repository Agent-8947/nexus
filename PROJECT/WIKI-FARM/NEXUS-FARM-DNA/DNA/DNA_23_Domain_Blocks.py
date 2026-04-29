#!/usr/bin/env python3
"""
NEXUS DOMAIN BLOCK LIBRARY v2.0 — CONTRACT-FIRST ARCHITECTURE
==============================================================
Each block declares:
  - input_type:  what data it consumes
  - output_type: what data it produces
  - test_input:  mock data for integration test

The composer wires blocks into PIPELINES (A.output → B.input),
not concatenations. Every agent gets a self-test that validates
the full pipeline with mock data.

Data Types (contracts):
  path         — filesystem Path to scan
  url          — HTTP URL string
  hostname     — domain/IP string
  text         — raw text string
  file_list    — list of file paths
  findings     — list[{"type","severity","detail","source"}]
  metrics      — list[float]
  stats        — {"count","mean","std","min","max",...}
  tech_stack   — list[{"tech","source","evidence"}]
  port_report  — list[{"port","open","service"}]
  system_info  — {"os","cpu_count","hostname",...}
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import textwrap


# ═══════════════════════════════════════════════════════════════════════════
# CONTRACT DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class BlockContract:
    """A single composable code block with defined I/O contract."""
    name: str
    domain: str
    input_type: str          # What this block consumes
    output_type: str         # What this block produces
    description: str         # Human-readable purpose
    code: str                # Python function code (def name(...) -> ...)
    test_input: str          # Python expression producing mock input
    test_assertion: str      # Python assertion on output


# ═══════════════════════════════════════════════════════════════════════════
# BLOCK REGISTRY — every block has a contract
# ═══════════════════════════════════════════════════════════════════════════

BLOCKS: List[BlockContract] = [

# ── SECURITY ─────────────────────────────────────────────────────────────

BlockContract(
    name="scan_secrets",
    domain="security",
    input_type="path",
    output_type="findings",
    description="Scan directory for leaked secrets (API keys, tokens, passwords)",
    code='''
SECRET_PATTERNS: Dict[str, tuple[str, str]] = {
    "aws_key":        (r"(?:AKIA|ASIA)[0-9A-Z]{16}", "CRITICAL"),
    "github_token":   (r"gh[pousr]_[A-Za-z0-9_]{36,255}", "CRITICAL"),
    "private_key":    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
    "generic_secret": (r"(?i)(?:secret|password|token|apikey)\\s*[:=]\\s*['\\"]+([A-Za-z0-9\\-_./+=]{8,64})", "HIGH"),
    "db_url":         (r"(?i)(?:postgres|mysql|mongodb|redis)://[^\\s\\'\\\"]{10,200}", "CRITICAL"),
    "jwt":            (r"eyJ[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}", "HIGH"),
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

def scan_secrets(target: Path) -> List[Dict[str, Any]]:
    """Scan files for leaked secrets. Returns standardized findings."""
    findings: List[Dict[str, Any]] = []
    for fpath in target.rglob("*"):
        if not fpath.is_file() or fpath.stat().st_size > 500_000:
            continue
        if any(s in fpath.parts for s in SKIP_DIRS):
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for rule_name, (pattern, severity) in SECRET_PATTERNS.items():
                for m in re.finditer(pattern, text):
                    line = text[:m.start()].count("\\n") + 1
                    findings.append({
                        "type": rule_name,
                        "severity": severity,
                        "detail": f"{rule_name} found at line {line}",
                        "source": str(fpath.relative_to(target)),
                        "line": line,
                        "preview": m.group(0)[:8] + "***",
                    })
        except Exception:
            pass
    return findings
''',
    test_input='Path(tempfile.mkdtemp())',
    test_assertion='isinstance(result, list)',
),

BlockContract(
    name="check_ssl",
    domain="security",
    input_type="hostname",
    output_type="findings",
    description="Check SSL certificate validity, extract issuer/expiry/SANs",
    code='''
def check_ssl(target: str) -> List[Dict[str, Any]]:
    """Check SSL certificate and return findings."""
    findings: List[Dict[str, Any]] = []
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=target) as s:
            s.settimeout(5)
            s.connect((target, 443))
            cert = s.getpeercert()
            expires = cert.get("notAfter", "")
            findings.append({
                "type": "ssl_valid", "severity": "INFO",
                "detail": f"SSL valid, expires {expires}",
                "source": target,
            })
            # Check expiry
            from datetime import datetime as _dt
            try:
                exp_date = _dt.strptime(expires, "%b %d %H:%M:%S %Y %Z")
                days_left = (exp_date - _dt.now()).days
                if days_left < 30:
                    findings.append({
                        "type": "ssl_expiring", "severity": "HIGH",
                        "detail": f"SSL expires in {days_left} days",
                        "source": target,
                    })
            except Exception:
                pass
    except Exception as e:
        findings.append({
            "type": "ssl_error", "severity": "CRITICAL",
            "detail": f"SSL check failed: {e}",
            "source": target,
        })
    return findings
''',
    test_input='"localhost"',
    test_assertion='isinstance(result, list) and all("type" in f and "severity" in f for f in result)',
),

BlockContract(
    name="hash_files",
    domain="security",
    input_type="path",
    output_type="findings",
    description="Compute integrity hashes (SHA256) for all files in directory",
    code='''
def hash_files(target: Path) -> List[Dict[str, Any]]:
    """Compute SHA256 hashes for files, returning as findings."""
    findings: List[Dict[str, Any]] = []
    for fpath in target.rglob("*"):
        if not fpath.is_file() or fpath.stat().st_size > 2_000_000:
            continue
        if ".git" in fpath.parts:
            continue
        try:
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            findings.append({
                "type": "file_hash", "severity": "INFO",
                "detail": f"SHA256: {sha[:16]}...",
                "source": str(fpath.relative_to(target)),
                "hash": sha,
            })
        except Exception:
            pass
    return findings
''',
    test_input='Path(tempfile.mkdtemp())',
    test_assertion='isinstance(result, list)',
),

# ── OSINT ────────────────────────────────────────────────────────────────

BlockContract(
    name="dns_recon",
    domain="osint",
    input_type="hostname",
    output_type="findings",
    description="DNS resolution with IP collection",
    code='''
def dns_recon(target: str) -> List[Dict[str, Any]]:
    """Resolve hostname and return findings."""
    findings: List[Dict[str, Any]] = []
    try:
        info = socket.getaddrinfo(target, None)
        ips = list(set(addr[4][0] for addr in info))
        for ip in ips:
            findings.append({
                "type": "dns_record", "severity": "INFO",
                "detail": f"Resolved to {ip}",
                "source": target,
                "ip": ip,
            })
    except socket.gaierror as e:
        findings.append({
            "type": "dns_error", "severity": "MEDIUM",
            "detail": f"DNS resolution failed: {e}",
            "source": target,
        })
    return findings
''',
    test_input='"localhost"',
    test_assertion='isinstance(result, list)',
),

BlockContract(
    name="http_fingerprint",
    domain="osint",
    input_type="url",
    output_type="tech_stack",
    description="Fingerprint web technology stack via HTTP headers and body patterns",
    code='''
_TECH_HEADERS = {"X-Powered-By": "framework", "Server": "server", "X-Generator": "cms"}
_BODY_SIGS = {
    r"wp-content/|wp-includes/": "WordPress",
    r"drupal\\.js|Drupal\\.settings": "Drupal",
    r"__next|_next/static": "Next.js",
    r"django|csrfmiddlewaretoken": "Django",
    r"laravel_session": "Laravel",
    r"flask|Werkzeug": "Flask",
}

def http_fingerprint(target: str) -> List[Dict[str, Any]]:
    """Fingerprint web technology stack. Returns tech_stack."""
    techs: List[Dict[str, Any]] = []
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = target if target.startswith("http") else f"https://{target}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NEXUS-Recon"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            headers = {k: v for k, v in resp.getheaders()}
            body = resp.read().decode("utf-8", errors="ignore")[:50000]
            for h, label in _TECH_HEADERS.items():
                if h in headers:
                    techs.append({"tech": f"{label}: {headers[h]}", "source": "header", "evidence": headers[h]})
            for pattern, name in _BODY_SIGS.items():
                if re.search(pattern, body, re.IGNORECASE):
                    techs.append({"tech": name, "source": "body_pattern", "evidence": pattern})
    except Exception as e:
        techs.append({"tech": "error", "source": "http_error", "evidence": str(e)})
    return techs
''',
    test_input='"http://localhost:99999"',
    test_assertion='isinstance(result, list)',
),

BlockContract(
    name="probe_endpoints",
    domain="osint",
    input_type="url",
    output_type="findings",
    description="Probe for common sensitive endpoints (.env, /admin, /api, etc.)",
    code='''
_SENSITIVE_PATHS = [
    ("/.env", "CRITICAL"), ("/.git/config", "CRITICAL"), ("/wp-admin/", "HIGH"),
    ("/admin/", "HIGH"), ("/api/", "MEDIUM"), ("/swagger/", "MEDIUM"),
    ("/graphql", "MEDIUM"), ("/actuator/health", "HIGH"), ("/server-status", "HIGH"),
    ("/robots.txt", "INFO"), ("/sitemap.xml", "INFO"),
]

def probe_endpoints(target: str) -> List[Dict[str, Any]]:
    """Probe for common sensitive endpoints. Returns findings."""
    findings: List[Dict[str, Any]] = []
    base = target.rstrip("/") if target.startswith("http") else f"https://{target}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for path, severity in _SENSITIVE_PATHS:
        url = base + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                if resp.status < 400:
                    findings.append({
                        "type": "exposed_endpoint", "severity": severity,
                        "detail": f"Accessible: {path} (HTTP {resp.status})",
                        "source": url,
                    })
        except urllib.error.HTTPError as e:
            if e.code < 404:  # 401/403 still interesting
                findings.append({
                    "type": "protected_endpoint", "severity": "INFO",
                    "detail": f"Protected: {path} (HTTP {e.code})",
                    "source": url,
                })
        except Exception:
            pass
    return findings
''',
    test_input='"http://localhost:99999"',
    test_assertion='isinstance(result, list)',
),

# ── AI / ANALYSIS ────────────────────────────────────────────────────────

BlockContract(
    name="detect_anomalies",
    domain="ai",
    input_type="metrics",
    output_type="findings",
    description="Z-Score + IQR anomaly detection on numeric series",
    code='''
def detect_anomalies(target: List[float]) -> List[Dict[str, Any]]:
    """Detect anomalies using Z-Score and IQR methods. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if len(target) < 5:
        return findings
    mean = sum(target) / len(target)
    var = sum((v - mean) ** 2 for v in target) / len(target)
    std = math.sqrt(var) if var > 0 else 1e-8
    # Z-Score detection
    for i, v in enumerate(target):
        z = abs(v - mean) / std
        if z >= 3.0:
            findings.append({
                "type": "anomaly_zscore", "severity": "CRITICAL" if z >= 4.0 else "WARNING",
                "detail": f"Index {i}: value={v:.3f}, z-score={z:.2f}",
                "source": f"index_{i}",
                "index": i, "value": v, "score": round(z, 3),
            })
    # IQR detection
    s = sorted(target)
    n = len(s)
    q1 = s[n // 4]
    q3 = s[3 * n // 4]
    iqr = q3 - q1
    if iqr > 1e-8:
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        for i, v in enumerate(target):
            if v < lower or v > upper:
                dist = max(abs(v - lower), abs(v - upper)) / iqr
                findings.append({
                    "type": "anomaly_iqr", "severity": "HIGH",
                    "detail": f"Index {i}: value={v:.3f}, IQR distance={dist:.2f}",
                    "source": f"index_{i}",
                    "index": i, "value": v, "score": round(dist, 3),
                })
    return findings
''',
    test_input='[1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 100.0, 1.0, 0.98]',
    test_assertion='isinstance(result, list) and any(f["severity"] in ("CRITICAL","WARNING","HIGH") for f in result)',
),

BlockContract(
    name="compute_stats",
    domain="ai",
    input_type="metrics",
    output_type="stats",
    description="Descriptive statistics (mean, median, std, quartiles, IQR)",
    code='''
def compute_stats(target: List[float]) -> Dict[str, Any]:
    """Compute descriptive statistics for a numeric series. Returns stats."""
    if not target:
        return {"count": 0, "error": "empty input"}
    s = sorted(target)
    n = len(s)
    mean = sum(s) / n
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    var = sum((v - mean) ** 2 for v in s) / n
    std = math.sqrt(var)
    q1 = s[n // 4] if n >= 4 else s[0]
    q3 = s[3 * n // 4] if n >= 4 else s[-1]
    return {
        "count": n, "mean": round(mean, 4), "median": round(median, 4),
        "std": round(std, 4), "min": s[0], "max": s[-1],
        "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4),
    }
''',
    test_input='[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]',
    test_assertion='isinstance(result, dict) and "mean" in result and result["count"] == 8',
),

BlockContract(
    name="text_similarity",
    domain="ai",
    input_type="text",
    output_type="stats",
    description="TF-based cosine similarity between text sections",
    code='''
def text_similarity(target: str) -> Dict[str, Any]:
    """Split text in half and compute self-similarity. Returns stats."""
    mid = len(target) // 2
    a, b = target[:mid], target[mid:]
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(a), tokenize(b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values())) or 1e-8
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values())) or 1e-8
    similarity = dot / (norm_a * norm_b)
    return {
        "similarity": round(similarity, 4),
        "tokens_a": len(fa), "tokens_b": len(fb),
        "method": "cosine_tf",
    }
''',
    test_input='"hello world foo bar hello world baz qux"',
    test_assertion='isinstance(result, dict) and "similarity" in result',
),

# ── INFRA ────────────────────────────────────────────────────────────────

BlockContract(
    name="check_ports",
    domain="infra",
    input_type="hostname",
    output_type="port_report",
    description="TCP port scanner for common service ports",
    code='''
_COMMON_PORTS = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
                 5432: "Postgres", 6379: "Redis", 8080: "HTTP-Alt",
                 8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB"}

def check_ports(target: str) -> List[Dict[str, Any]]:
    """Check which TCP ports are open on a host. Returns port_report."""
    results: List[Dict[str, Any]] = []
    for port, service in _COMMON_PORTS.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                is_open = s.connect_ex((target, port)) == 0
                results.append({"port": port, "open": is_open, "service": service})
        except Exception:
            results.append({"port": port, "open": False, "service": service, "error": True})
    return results
''',
    test_input='"127.0.0.1"',
    test_assertion='isinstance(result, list) and all("port" in r and "open" in r for r in result)',
),

BlockContract(
    name="system_info",
    domain="infra",
    input_type="hostname",
    output_type="system_info",
    description="Collect local system information (OS, CPU, Python version)",
    code='''
def system_info(target: str) -> Dict[str, Any]:
    """Collect system information. Returns system_info."""
    return {
        "os": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "python": platform.python_version(),
        "cpu_count": os.cpu_count() or 0,
        "hostname": platform.node(),
        "queried_target": target,
    }
''',
    test_input='"localhost"',
    test_assertion='isinstance(result, dict) and "os" in result and "cpu_count" in result',
),

BlockContract(
    name="process_list",
    domain="infra",
    input_type="hostname",
    output_type="findings",
    description="List running processes (cross-platform)",
    code='''
def process_list(target: str) -> List[Dict[str, Any]]:
    """List running processes. Returns findings."""
    findings: List[Dict[str, Any]] = []
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["tasklist", "/FO", "CSV", "/NH"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[0]}",
                        "source": target,
                    })
        else:
            out = subprocess.check_output(["ps", "aux", "--no-headers"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[10][:60]}",
                        "source": target,
                    })
    except Exception as e:
        findings.append({"type": "process_error", "severity": "MEDIUM",
                         "detail": str(e), "source": target})
    return findings
''',
    test_input='"localhost"',
    test_assertion='isinstance(result, list)',
),

# ── WEB ──────────────────────────────────────────────────────────────────

BlockContract(
    name="extract_links",
    domain="web",
    input_type="url",
    output_type="findings",
    description="Extract all links from a web page",
    code='''
class _LinkParser(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.links: List[str] = []
    def handle_starttag(self, tag, attrs):
        if tag in ("a", "link", "script", "img"):
            for n, v in attrs:
                if n in ("href", "src") and v:
                    self.links.append(urljoin(self.base, v))

def extract_links(target: str) -> List[Dict[str, Any]]:
    """Extract all links from a web page. Returns findings."""
    findings: List[Dict[str, Any]] = []
    url = target if target.startswith("http") else f"https://{target}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
        p = _LinkParser(url)
        p.feed(body)
        for link in set(p.links):
            findings.append({
                "type": "link", "severity": "INFO",
                "detail": link[:200], "source": url,
            })
    except Exception as e:
        findings.append({"type": "link_error", "severity": "MEDIUM",
                         "detail": str(e), "source": url})
    return findings
''',
    test_input='"http://localhost:99999"',
    test_assertion='isinstance(result, list)',
),

# ── DATA ─────────────────────────────────────────────────────────────────

BlockContract(
    name="analyze_csv",
    domain="data",
    input_type="path",
    output_type="stats",
    description="Analyze CSV file structure with column type detection",
    code='''
def analyze_csv(target: Path) -> Dict[str, Any]:
    """Analyze CSV file(s) in directory. Returns stats."""
    csv_files = list(target.rglob("*.csv")) if target.is_dir() else [target]
    if not csv_files:
        return {"error": "no CSV files found", "count": 0}
    all_stats: Dict[str, Any] = {"files_analyzed": len(csv_files), "columns": {}}
    for csv_file in csv_files[:5]:
        try:
            with open(csv_file, encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = [r for i, r in enumerate(reader) if i < 5000]
            for col in headers:
                nums = []
                for r in rows:
                    try: nums.append(float(r.get(col, "")))
                    except: pass
                if nums:
                    all_stats["columns"][col] = {
                        "type": "numeric", "count": len(nums),
                        "mean": round(sum(nums) / len(nums), 3),
                        "min": min(nums), "max": max(nums),
                    }
                else:
                    all_stats["columns"][col] = {"type": "text", "unique": len(set(r.get(col, "") for r in rows))}
        except Exception:
            pass
    return all_stats
''',
    test_input='Path(tempfile.mkdtemp())',
    test_assertion='isinstance(result, dict)',
),

BlockContract(
    name="store_findings_db",
    domain="data",
    input_type="findings",
    output_type="stats",
    description="Store findings in SQLite database and return summary",
    code='''
def store_findings_db(target: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Store findings in a temporary SQLite database. Returns stats."""
    db_path = Path(tempfile.mkdtemp()) / "findings.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, severity TEXT, detail TEXT, source TEXT, ts TEXT
    )""")
    for f in target:
        conn.execute("INSERT INTO findings (type, severity, detail, source, ts) VALUES (?,?,?,?,?)",
                     (f.get("type",""), f.get("severity",""), f.get("detail",""),
                      f.get("source",""), datetime.now().isoformat()))
    conn.commit()
    # Summary query
    cursor = conn.execute("SELECT severity, COUNT(*) FROM findings GROUP BY severity")
    by_severity = dict(cursor.fetchall())
    total = conn.execute("SELECT COUNT(*) FROM findings").fetchone()[0]
    conn.close()
    return {"db_path": str(db_path), "total_stored": total, "by_severity": by_severity}
''',
    test_input='[{"type":"test","severity":"INFO","detail":"mock","source":"test"}]',
    test_assertion='isinstance(result, dict) and result["total_stored"] == 1',
),

# ── HARDWARE ─────────────────────────────────────────────────────────────

BlockContract(
    name="find_serial_ports",
    domain="hardware",
    input_type="hostname",
    output_type="findings",
    description="Discover available serial ports (Windows/Linux)",
    code='''
def find_serial_ports(target: str) -> List[Dict[str, Any]]:
    """Discover available serial ports. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\\DEVICEMAP\\SERIALCOMM")
            i = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, i)
                    findings.append({"type": "serial_port", "severity": "INFO",
                                     "detail": f"{val} ({name})", "source": target})
                    i += 1
                except OSError:
                    break
        except Exception:
            findings.append({"type": "serial_scan", "severity": "INFO",
                             "detail": "No serial ports found (Windows)", "source": target})
    else:
        for p in Path("/dev").glob("tty*"):
            if any(x in p.name for x in ("USB", "ACM", "AMA")):
                findings.append({"type": "serial_port", "severity": "INFO",
                                 "detail": str(p), "source": target})
    return findings
''',
    test_input='"localhost"',
    test_assertion='isinstance(result, list)',
),

]

# ── DRONE / UAV ──────────────────────────────────────────────────────────
BLOCKS.extend([
    BlockContract(
        name="read_telemetry",
        domain="drone",
        input_type="hostname",  # usually comm port or udp connection string
        output_type="metrics",
        description="Read UAV telemetry stream (simulated MAVLink)",
        code='''
def read_telemetry(target: str) -> List[Dict[str, Any]]:
    """Connect to MAVLink endpoint and read telemetry. Returns metrics."""
    # Simulated MAVLink stream for safety/testing
    import random
    findings: List[Dict[str, Any]] = []
    try:
        # Check connection format
        if not target.startswith("udp:") and not target.startswith("tcp:") and "COM" not in target and "tty" not in target:
            findings.append({"type": "telemetry_error", "severity": "CRITICAL", "detail": "Invalid MAVLink connection string", "source": target})
            return findings
            
        alt = random.uniform(90.0, 110.0)
        heading = random.uniform(0.0, 360.0)
        gps_sats = random.randint(5, 12)
        batt_v = random.uniform(10.5, 12.6)
        
        findings.append({"type": "telemetry_alt", "severity": "INFO", "detail": f"Altitude: {alt:.2f}m", "source": target, "value": alt})
        findings.append({"type": "telemetry_hdg", "severity": "INFO", "detail": f"Heading: {heading:.1f}deg", "source": target, "value": heading})
        
        sev = "CRITICAL" if gps_sats < 6 else "INFO"
        findings.append({"type": "telemetry_gps", "severity": sev, "detail": f"Sats: {gps_sats}", "source": target, "value": float(gps_sats)})
        
        sev = "HIGH" if batt_v < 11.1 else "INFO"
        findings.append({"type": "telemetry_batt", "severity": sev, "detail": f"Voltage: {batt_v:.2f}V", "source": target, "value": batt_v})
    except Exception as e:
        findings.append({"type": "telemetry_sys_error", "severity": "CRITICAL", "detail": str(e), "source": target})
    return findings
''',
        test_input='"udp:127.0.0.1:14550"',
        test_assertion='isinstance(result, list) and any(f["type"] == "telemetry_alt" for f in result)'
    ),
    
    BlockContract(
        name="check_geofence",
        domain="drone",
        input_type="metrics",
        output_type="findings",
        description="Validate telemetry against geofence restrictions",
        code='''
def check_geofence(metrics: List[float]) -> List[Dict[str, Any]]:
    """Validate UAV telemetry metrics against dynamic geofence rules."""
    findings: List[Dict[str, Any]] = []
    MAX_ALTITUDE = 120.0 # meters
    if metrics and metrics[0] > MAX_ALTITUDE:
        findings.append({"type": "geofence_breach", "severity": "CRITICAL", "detail": f"Altitude {metrics[0]:.1f}m > limit", "source": "Geo"})
    return findings
''',
        test_input='[150.0]',
        test_assertion='isinstance(result, list)'
    ),

    BlockContract(
        name="mavsdk_telemetry",
        domain="drone",
        input_type="hostname",
        output_type="metrics",
        description="Connect to drone via MAVSDK and fetch live telemetry",
        code='''
def mavsdk_telemetry(target: str) -> List[Dict[str, Any]]:
    """Fetch live UAV telemetry using MAVSDK."""
    import asyncio
    try:
        from mavsdk import System
    except ImportError:
        return [{"type": "dep_err", "severity": "HIGH", "detail": "mavsdk missing", "source": "MAVSDK"}]

    findings: List[Dict[str, Any]] = []
    async def capture():
        drone = System()
        await drone.connect(system_address=target if "://" in target else f"udp://:{target}")
        async for pos in drone.telemetry.position():
            findings.append({"type": "mav_alt", "severity": "INFO", "value": pos.relative_altitude_m, "source": "MAVSDK"})
            break
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait_for(capture(), timeout=5.0))
        loop.close()
    except Exception as e:
        findings.append({"type": "mav_err", "severity": "WARNING", "detail": str(e), "source": "MAVSDK"})
    return findings
''',
        test_input='"14540"',
        test_assertion='isinstance(result, list)'
    ),

    BlockContract(
        name="mavsdk_action",
        domain="drone",
        input_type="findings",
        output_type="findings",
        description="Execute MAVSDK commands (RTL/Land) based on threats",
        code='''
def mavsdk_action(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Send MAVSDK commands based on findings."""
    import asyncio
    try:
        from mavsdk import System
    except ImportError: return []
    critical = any(f.get("severity") == "CRITICAL" for f in findings)
    async def cmd():
        drone = System()
        await drone.connect()
        if critical: await drone.action.return_to_launch()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait_for(cmd(), timeout=3.0))
        loop.close()
    except: pass
    return [{"type": "mav_cmd_sent", "severity": "INFO", "detail": "RTL" if critical else "Idle"}]
''',
        test_input='[]',
        test_assertion='isinstance(result, list)'
    ),
])

# ═══════════════════════════════════════════════════════════════════════════
# PIPELINE COMPATIBILITY MATRIX
# Which output_type can flow into which input_type?
# ═══════════════════════════════════════════════════════════════════════════

COMPATIBLE_FLOWS: Dict[str, List[str]] = {
    "findings": ["findings"],      # findings → aggregate into more findings
    "tech_stack": ["findings"],     # tech_stack can be treated as findings
    "port_report": ["findings"],   # port_report can be treated as findings
    "metrics": ["findings"],       # metrics can fallthrough to findings analysis
    "stats": [],                    # stats is a terminal output
    "system_info": [],             # system_info is a terminal output
}


# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS PER DOMAIN
# ═══════════════════════════════════════════════════════════════════════════

DOMAIN_IMPORTS: Dict[str, str] = {
    "security": "import re, hashlib, socket, ssl",
    "osint":    "import re, socket, ssl, urllib.request, urllib.error",
    "ai":       "import re, math",
    "infra":    "import os, re, socket, platform, subprocess",
    "web":      "import re, ssl, urllib.request, urllib.error\nfrom html.parser import HTMLParser\nfrom urllib.parse import urljoin",
    "data":     "import re, csv, sqlite3",
    "hardware": "import re, platform, subprocess",
    "drone":    "import time, random, asyncio",
}


def get_blocks_for_domains(domain_a: str, domain_b: str) -> List[BlockContract]:
    """Get all blocks matching two domains, deduplicated."""
    seen = set()
    result = []
    for b in BLOCKS:
        if b.domain in (domain_a, domain_b) and b.name not in seen:
            seen.add(b.name)
            result.append(b)
    return result


def _build_pipeline_logic(blocks: List[BlockContract], input_type: str) -> List[List[BlockContract]]:
    """
    Build pipeline stages: blocks that accept `input_type` run first,
    then blocks that accept their outputs run next.
    """
    stages: List[List[BlockContract]] = []
    available_types = {input_type}

    remaining = list(blocks)
    while remaining:
        stage = [b for b in remaining if b.input_type in available_types]
        if not stage:
            break
        stages.append(stage)
        for b in stage:
            remaining.remove(b)
            available_types.add(b.output_type)
            # Check COMPATIBLE_FLOWS for transitive types
            for compat in COMPATIBLE_FLOWS.get(b.output_type, []):
                available_types.add(compat)

    return stages


def compose_agent(child_id: str, mission: str, parent_a: str, parent_b: str,
                  domain_a: str, domain_b: str, role: str, generation: int) -> str:
    """Compose a PIPELINE agent from domain blocks with contracts and integration test."""

    blocks = get_blocks_for_domains(domain_a, domain_b)
    if not blocks:
        # Fallback to infra blocks
        blocks = get_blocks_for_domains("infra", "infra")

    # Determine primary input type based on role
    if role in ("collector", "payload"):
        primary_input = "path"
    elif role in ("presentation", "library"):
        primary_input = "url"
    else:
        primary_input = "hostname"

    # Build import set
    imports = set()
    for d in [domain_a, domain_b]:
        if d in DOMAIN_IMPORTS:
            imports.add(DOMAIN_IMPORTS[d])

    # Build pipeline stages
    stages = _build_pipeline_logic(blocks, primary_input)
    # Add unplaced blocks as independent stage
    placed_names = {b.name for stage in stages for b in stage}
    unplaced = [b for b in blocks if b.name not in placed_names]
    if unplaced:
        stages.append(unplaced)

    # ── Generate code ────────────────────────────────────────────────────

    lines = []
    lines.append(f'#!/usr/bin/env python3')
    lines.append(f'"""')
    lines.append(f'{child_id} [NEXUS SYNTHESIZED Gen-{generation}]')
    lines.append(f'Mission: {mission}')
    lines.append(f'Heritage: {parent_a} + {parent_b}')
    lines.append(f'Role: {role} | Domains: {domain_a} & {domain_b}')
    lines.append(f'')
    lines.append(f'I/O Contract:')
    lines.append(f'  Input:  {primary_input} (from CLI --target)')
    lines.append(f'  Output: JSON report with typed findings/stats')
    lines.append(f'')
    lines.append(f'Pipeline ({len(stages)} stages, {len(blocks)} blocks):')
    for i, stage in enumerate(stages):
        names = ", ".join(b.name for b in stage)
        lines.append(f'  Stage {i+1}: [{names}]')
    lines.append(f'"""')
    lines.append(f'')
    lines.append(f'import sys')
    lines.append(f'import json')
    lines.append(f'import logging')
    lines.append(f'import argparse')
    lines.append(f'import tempfile')
    lines.append(f'from pathlib import Path')
    lines.append(f'from datetime import datetime')
    lines.append(f'from typing import List, Dict, Any')
    for imp in sorted(imports):
        lines.append(imp)
    lines.append(f'')
    lines.append(f'__all__ = ["main", "Pipeline"]')
    lines.append(f'')
    lines.append(f'')
    lines.append(f'logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")')
    lines.append(f'logger = logging.getLogger("{child_id[:60]}")')
    lines.append(f'')
    # Inject universal executor into the generated file's global scope
    lines.append(f'def __nexus_execute__(func, arg, output_type, findings_list, stats_dict, errors_list):')
    lines.append(f'    try:')
    lines.append(f'        _result = func(arg)')
    lines.append(f'        if output_type == "findings":')
    lines.append(f'            if isinstance(_result, list): findings_list.extend(_result)')
    lines.append(f'            logger.info(f"  [{{func.__name__}}] {{len(_result) if isinstance(_result, list) else 0}} findings")')
    lines.append(f'        elif output_type in ("stats", "tech_stack", "port_report", "system_info", "report"):')
    lines.append(f'            if isinstance(_result, dict): stats_dict.update(_result)')
    lines.append(f'            if output_type == "port_report" and isinstance(_result, list):')
    lines.append(f'                for item in _result:')
    lines.append(f'                    if isinstance(item, dict) and "type" not in item:')
    lines.append(f'                        item.update({{"type": func.__name__, "severity": "INFO", "detail": str(item), "source": "nexus_pipeline"}})')
    lines.append(f'                    findings_list.append(item)')
    lines.append(f'            logger.info(f"  [{{func.__name__}}] OK")')
    lines.append(f'        else:')
    lines.append(f'            if isinstance(_result, list): findings_list.extend(_result)')
    lines.append(f'            elif isinstance(_result, dict): stats_dict.update(_result)')
    lines.append(f'            logger.info(f"  [{{func.__name__}}] OK")')
    lines.append(f'    except Exception as e:')
    lines.append(f'        errors_list.append(f"{{func.__name__}}: {{e}}")')
    lines.append(f'        logger.warning(f"  [{{func.__name__}}] SKIP: {{e}}")')
    lines.append(f'')
    lines.append(f'')

    # ── Block functions ──────────────────────────────────────────────────
    for block in blocks:
        lines.append(f'# ── [{block.domain.upper()}] {block.description} ──')
        lines.append(block.code.strip())
        lines.append(f'')
        lines.append(f'')

    # ── Role-enforced class ────────────────────────────────────────────────
    # Import role contract system
    try:
        from DNA_25_Role_Contracts import get_contract, generate_role_class
        contract = get_contract(role)
        class_name = contract.class_name
        method_name = contract.required_method
    except ImportError:
        class_name = "Pipeline"
        method_name = "run"

    # Build block calls as indented code for inside the role method
    block_call_lines = []
    for stage_idx, stage in enumerate(stages):
        block_call_lines.append(f'        # -- Stage {stage_idx + 1} --')
        for block in stage:
            findings_ref = "self.findings" if method_name == "collect" else \
                           "self.enriched" if method_name == "analyze" else \
                           "self.all_findings"

            # Map input arguments based on role parameter and block input_type
            if method_name == "render":
                if block.input_type == "findings": arg = findings_ref
                elif block.input_type == "metrics": arg = f"[f.get('value', 0) for f in {findings_ref} if 'value' in f] or [0.0]"
                else: arg = 'report.get("target", "unknown")'
            elif method_name == "analyze":
                if block.input_type == "findings": arg = "findings"
                elif block.input_type == "metrics": arg = f"[f.get('value', 0) for f in findings if 'value' in f] or [0.0]"
                else: arg = 'findings[0].get("source", "unknown") if findings else "unknown"'
            else:
                if block.input_type == "findings": arg = findings_ref
                elif block.input_type == "metrics": arg = f"[f.get('value', 0) for f in {findings_ref} if 'value' in f] or [0.0]"
                else: arg = "str(target)" if block.input_type == "text" else "target"



            # Elegantly call the executor
            block_call_lines.append(f'        __nexus_execute__({block.name}, {arg}, "{block.output_type}", {findings_ref}, getattr(self, "all_stats", {{}}), self.errors)')

    block_calls_str = "\n".join(block_call_lines)

    # Generate full class with role contract
    try:
        role_class_code = generate_role_class(contract, child_id, block_calls_str)
        lines.append(role_class_code)
    except Exception:
        # Fallback to generic Pipeline
        lines.append(f'class {class_name}:')
        lines.append(f'    """Orchestrates {len(blocks)} blocks in {len(stages)} stages."""')
        lines.append(f'')
        lines.append(f'    def __init__(self):')
        lines.append(f'        self.all_findings: List[Dict[str, Any]] = []')
        lines.append(f'        self.all_stats: Dict[str, Any] = {{}}')
        lines.append(f'        self.errors: List[str] = []')
        lines.append(f'')
        lines.append(f'    def {method_name}(self, target) -> Dict[str, Any]:')
        lines.append(block_calls_str)
        lines.append(f'        risk = {{"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}}')
        lines.append(f'        for f in self.all_findings:')
        lines.append(f'            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1')
        lines.append(f'        return {{"agent": "{child_id}", "findings": self.all_findings, "stats": self.all_stats, "errors": self.errors, "risk_summary": risk}}')
    lines.append(f'')
    lines.append(f'')

    # ── Integration test ─────────────────────────────────────────────────
    lines.append(f'def _integration_test():')
    lines.append(f'    """End-to-end pipeline test with mock data."""')
    lines.append(f'    agent = {class_name}()')

    # Use first block's test_input as pipeline input
    first_test = blocks[0].test_input if blocks else '"test"'
    lines.append(f'    test_target = {first_test}')

    # Call the role-specific method
    if method_name == "collect":
        lines.append(f'    result = agent.collect(test_target)')
        lines.append(f'    assert isinstance(result, list), "collect() must return List[Finding]"')
        lines.append(f'    for f in result:')
        lines.append(f'        assert "type" in f, f"Finding missing type"')
        lines.append(f'        assert "severity" in f, f"Finding missing severity"')
        lines.append(f'    logger.info(f"[TEST] {class_name}.collect() OK: {{len(result)}} findings")')
    elif method_name == "analyze":
        lines.append(f'    mock_findings = [{{"type":"test","severity":"INFO","detail":"mock","source":"test"}}]')
        lines.append(f'    result = agent.analyze(mock_findings)')
        lines.append(f'    assert isinstance(result, list), "analyze() must return List[Finding]"')
        lines.append(f'    logger.info(f"[TEST] {class_name}.analyze() OK: {{len(result)}} findings")')
    elif method_name == "insert":
        lines.append(f'    mock_findings = [{{"type":"test","severity":"INFO","detail":"mock","source":"test"}}]')
        lines.append(f'    result = agent.insert(mock_findings)')
        lines.append(f'    assert isinstance(result, dict), "insert() must return dict"')
        lines.append(f'    assert "total_stored" in result, "insert() must return total_stored"')
        lines.append(f'    logger.info(f"[TEST] {class_name}.insert() OK: {{result}}")')
    elif method_name == "render":
        lines.append(f'    mock_report = {{"target": "test", "findings": [{{ "type": "test", "severity": "INFO", "value": 100, "detail": "test", "source": "test" }}]}}')
        lines.append(f'    result = agent.render(mock_report)')
        lines.append(f'    assert isinstance(result, str) and len(result) > 0, "render() must return non-empty string"')
        lines.append(f'    logger.info(f"[TEST] {class_name}.render() OK")')
    else:
        lines.append(f'    result = agent.{method_name}(test_target)')
        lines.append(f'    assert isinstance(result, dict), "{method_name}() must return dict"')
        lines.append(f'    assert "findings" in result, "{method_name}() must return findings"')
        lines.append(f'    logger.info(f"[TEST] {class_name}.{method_name}() OK")')
    lines.append(f'    return True')
    lines.append(f'')
    lines.append(f'')

    # ── Main ─────────────────────────────────────────────────────────────
    lines.append(f'def main():')
    lines.append(f'    parser = argparse.ArgumentParser(description="{child_id}")')
    lines.append(f'    parser.add_argument("--target", default=None, help="Target ({primary_input})")')
    lines.append(f'    parser.add_argument("--output", default="report.json", help="Output JSON report")')
    lines.append(f'    parser.add_argument("--test", action="store_true", help="Run integration test")')
    lines.append(f'    args = parser.parse_args()')
    lines.append(f'')
    lines.append(f'    if args.test:')
    lines.append(f'        _integration_test()')
    lines.append(f'        return')
    lines.append(f'')
    lines.append(f'    if not args.target:')
    lines.append(f'        parser.error("--target is required (use --test for self-test)")')
    lines.append(f'')

    # Convert target to proper type
    if primary_input == "path":
        lines.append(f'    target = Path(args.target).resolve()')
    else:
        lines.append(f'    target = args.target')

    lines.append(f'')
    lines.append(f'    agent = {class_name}()')
    if method_name in ("collect", "execute"):
        lines.append(f'    findings = agent.{method_name}(target)')
        lines.append(f'    report = {{"agent": "{child_id}", "findings": findings, "summary": agent.summary()}}')
    elif method_name == "analyze":
        lines.append(f'    # Analyzer expects pre-collected findings')
        lines.append(f'    report_data = agent.analyze([{{ "type": "standalone", "severity": "INFO", "detail": str(target), "source": str(target) }}])')
        lines.append(f'    report = {{"agent": "{child_id}", "findings": report_data, "summary": agent.summary()}}')
    elif method_name == "render":
        lines.append(f'    # Presentation expects a report object')
        lines.append(f'    mock_report = {{"target": str(target), "findings": [], "stats": {{}}}}')
        lines.append(f'    report_str = agent.render(mock_report)')
        lines.append(f'    print(report_str)')
        lines.append(f'    return')
    else:
        lines.append(f'    report = agent.{method_name}(target)')
    
    lines.append(f'')
    lines.append(f'    # Display summary if report is a dict with findings')
    lines.append(f'    if isinstance(report, dict) and "findings" in report:')
    lines.append(f'        crits = [f for f in report["findings"] if f.get("severity") in ("CRITICAL", "HIGH")]')
    lines.append(f'        if crits:')
    lines.append(f'            print(f"\\n{{\'=\'*60}}")')
    lines.append(f'            print(f"⚠ {{len(crits)}} CRITICAL/HIGH FINDINGS:")')
    lines.append(f'            print(f"{{\'=\'*60}}")')
    lines.append(f'            for f in crits[:10]:')
    lines.append(f'                print(f"  [{{f.get(\'severity\')}}] {{f.get(\'detail\')}}")')
    lines.append(f'')
    lines.append(f'')
    lines.append(f'if __name__ == "__main__":')
    lines.append(f'    try:')
    lines.append(f'        main()')
    lines.append(f'    except KeyboardInterrupt:')
    lines.append(f'        sys.exit(0)')
    lines.append(f'    except Exception as e:')
    lines.append(f'        logger.critical(f"FATAL: {{e}}")')
    lines.append(f'        sys.exit(1)')
    lines.append(f'')

    return "\n".join(lines)


if __name__ == "__main__":
    # Self-test: generate and validate
    import ast as _ast
    code = compose_agent(
        child_id="TEST_PIPELINE",
        mission="Integration test",
        parent_a="CRAWL4AI", parent_b="METASPLOIT",
        domain_a="osint", domain_b="security",
        role="collector", generation=1,
    )
    _ast.parse(code)
    loc = len([l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")])
    print(f"[OK] Composed pipeline agent: {len(code)} bytes, {loc} code lines")
    print(f"[OK] Syntax validation PASSED")

    # Cross-domain test
    code2 = compose_agent(
        child_id="TEST_CROSS",
        mission="Cross test",
        parent_a="GRAFANA", parent_b="GITLEAKS",
        domain_a="infra", domain_b="security",
        role="analyzer", generation=2,
    )
    _ast.parse(code2)
    loc2 = len([l for l in code2.split("\n") if l.strip() and not l.strip().startswith("#")])
    print(f"[OK] Cross-domain agent: {len(code2)} bytes, {loc2} code lines")
    print(f"[OK] All self-tests PASSED")
