#!/usr/bin/env python3
"""
HYBRID_LADYBIRD_x_BACKOFF__X__STABLE_DIFFUSION_WEBUI [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: HYBRID_LADYBIRD_x_BACKOFF + STABLE_DIFFUSION_WEBUI
Role: library | Domains: security & osint

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 6 blocks):
  Stage 1: [http_fingerprint, probe_endpoints]
  Stage 2: [scan_secrets, check_ssl, hash_files, dns_recon]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, hashlib, socket, ssl
import re, socket, ssl, urllib.request, urllib.error

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("HYBRID_LADYBIRD_x_BACKOFF__X__STABLE_DIFFUSION_WEBUI")


# ── [SECURITY] Scan directory for leaked secrets (API keys, tokens, passwords) ──
SECRET_PATTERNS: Dict[str, tuple[str, str]] = {
    "aws_key":        (r"(?:AKIA|ASIA)[0-9A-Z]{16}", "CRITICAL"),
    "github_token":   (r"gh[pousr]_[A-Za-z0-9_]{36,255}", "CRITICAL"),
    "private_key":    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
    "generic_secret": (r"(?i)(?:secret|password|token|apikey)\s*[:=]\s*['\"]+([A-Za-z0-9\-_./+=]{8,64})", "HIGH"),
    "db_url":         (r"(?i)(?:postgres|mysql|mongodb|redis)://[^\s\'\"]{10,200}", "CRITICAL"),
    "jwt":            (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "HIGH"),
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
                    line = text[:m.start()].count("\n") + 1
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


# ── [SECURITY] Check SSL certificate validity, extract issuer/expiry/SANs ──
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


# ── [SECURITY] Compute integrity hashes (SHA256) for all files in directory ──
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


# ── [OSINT] DNS resolution with IP collection ──
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


# ── [OSINT] Fingerprint web technology stack via HTTP headers and body patterns ──
_TECH_HEADERS = {"X-Powered-By": "framework", "Server": "server", "X-Generator": "cms"}
_BODY_SIGS = {
    r"wp-content/|wp-includes/": "WordPress",
    r"drupal\.js|Drupal\.settings": "Drupal",
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


# ── [OSINT] Probe for common sensitive endpoints (.env, /admin, /api, etc.) ──
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


class Pipeline:
    """Orchestrates 6 blocks in 2 stages."""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """Execute full pipeline. Target type: url."""

        # ── Stage 1 ──
        try:
            result = http_fingerprint(target)
            self.all_stats["http_fingerprint"] = result
            logger.info(f"  [http_fingerprint] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"http_fingerprint: {e}")
            logger.warning(f"  [http_fingerprint] SKIP: {e}")
        try:
            result = probe_endpoints(target)
            self.all_findings.extend(result)
            logger.info(f"  [probe_endpoints] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"probe_endpoints: {e}")
            logger.warning(f"  [probe_endpoints] SKIP: {e}")

        # ── Stage 2 ──
        try:
            result = scan_secrets(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [scan_secrets] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"scan_secrets: {e}")
            logger.warning(f"  [scan_secrets] SKIP: {e}")
        try:
            result = check_ssl(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [check_ssl] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"check_ssl: {e}")
            logger.warning(f"  [check_ssl] SKIP: {e}")
        try:
            result = hash_files(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [hash_files] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"hash_files: {e}")
            logger.warning(f"  [hash_files] SKIP: {e}")
        try:
            result = dns_recon(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [dns_recon] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"dns_recon: {e}")
            logger.warning(f"  [dns_recon] SKIP: {e}")

        # ── Build report ──
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            sev = f.get("severity", "INFO")
            risk_summary[sev] = risk_summary.get(sev, 0) + 1

        return {
            "agent": "HYBRID_LADYBIRD_x_BACKOFF__X__STABLE_DIFFUSION_WEBUI",
            "version": "2.0-gen2",
            "timestamp": datetime.now().isoformat(),
            "pipeline_stages": 2,
            "blocks_executed": 6 - len(self.errors),
            "target": str(target),
            "risk_summary": risk_summary,
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
        }


def _integration_test():
    """End-to-end pipeline test with mock data."""
    pipe = Pipeline()
    test_target = Path(tempfile.mkdtemp())
    report = pipe.run(test_target)

    # Contract assertions
    assert isinstance(report, dict), "Report must be dict"
    assert "agent" in report, "Report must have agent field"
    assert "findings" in report, "Report must have findings field"
    assert "stats" in report, "Report must have stats field"
    assert "risk_summary" in report, "Report must have risk_summary"
    assert isinstance(report["findings"], list), "Findings must be list"
    for f in report["findings"]:
        assert "type" in f, f"Finding missing type: {f}"
        assert "severity" in f, f"Finding missing severity: {f}"
        assert "detail" in f, f"Finding missing detail: {f}"
        assert "source" in f, f"Finding missing source: {f}"
    logger.info(f"[TEST] Pipeline OK: {len(report['findings'])} findings, {len(report['errors'])} errors")
    return True


def main():
    parser = argparse.ArgumentParser(description="HYBRID_LADYBIRD_x_BACKOFF__X__STABLE_DIFFUSION_WEBUI")
    parser.add_argument("--target", default=None, help="Target (url)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = args.target

    pipe = Pipeline()
    report = pipe.run(target)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] {len(report['findings'])} findings → {output}")

    crits = [f for f in report["findings"] if f["severity"] in ("CRITICAL", "HIGH")]
    if crits:
        print(f"\n{'='*60}")
        print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
        print(f"{'='*60}")
        for f in crits[:10]:
            print(f"  [{f['severity']}] {f['detail']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
