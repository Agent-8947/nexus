#!/usr/bin/env python3
"""
KERAS__X__HYBRID_2026-AI-COLLEGE-JOBS_x_NLP [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: KERAS + HYBRID_2026-AI-COLLEGE-JOBS_x_NLP
Role: collector | Domains: ai & osint
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re, math, csv, statistics
import re, socket, urllib.request, urllib.error, ssl

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("KERAS__X__HYBRID_2026-AI-COLLEGE-JOBS_x_NLP")


# ── Statistical Z-Score anomaly detection ──
def detect_anomalies_zscore(values: list[float], threshold: float = 3.0) -> list[dict]:
    """Z-Score anomaly detection on numeric series."""
    import math
    if len(values) < 5:
        return []
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(var) if var > 0 else 1e-8
    anomalies = []
    for i, v in enumerate(values):
        z = abs(v - mean) / std
        if z >= threshold:
            anomalies.append({"index": i, "value": v, "zscore": round(z, 3),
                              "severity": "CRITICAL" if z >= 4 else "WARNING"})
    return anomalies


# ── TF-based cosine similarity between two texts ──
def cosine_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using word frequency."""
    import math, re
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(text_a), tokenize(text_b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values()))
    if norm_a < 1e-8 or norm_b < 1e-8:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)


# ── Descriptive statistics (mean, median, std, quartiles, IQR) ──
def compute_stats(values: list[float]) -> dict:
    """Compute descriptive statistics for a numeric series."""
    import math, statistics
    if not values:
        return {}
    s = sorted(values)
    n = len(s)
    mean = sum(s) / n
    median = statistics.median(s)
    std = statistics.stdev(s) if n > 1 else 0.0
    q1 = statistics.median(s[:n//2]) if n > 2 else s[0]
    q3 = statistics.median(s[(n+1)//2:]) if n > 2 else s[-1]
    return {"count": n, "mean": round(mean, 4), "median": round(median, 4),
            "std": round(std, 4), "min": s[0], "max": s[-1],
            "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4)}


# ── DNS resolution with IP collection and alias detection ──
def dns_resolve(hostname: str) -> dict:
    """Resolve hostname and gather DNS information."""
    import socket
    result = {"hostname": hostname, "ips": [], "aliases": [], "error": None}
    try:
        info = socket.getaddrinfo(hostname, None)
        result["ips"] = list(set(addr[4][0] for addr in info))
        try:
            host_info = socket.gethostbyname_ex(hostname)
            result["aliases"] = host_info[1]
        except Exception:
            pass
    except socket.gaierror as e:
        result["error"] = str(e)
    return result


# ── HTTP technology fingerprinting via headers and body patterns ──
TECH_HEADERS = {"X-Powered-By": "framework", "Server": "server", "X-Generator": "cms"}
BODY_SIGS = {
    r"wp-content/|wp-includes/": "WordPress",
    r"drupal\.js|Drupal\.settings": "Drupal",
    r"__next|_next/static": "Next.js",
    r"django|csrfmiddlewaretoken": "Django",
    r"laravel_session": "Laravel",
}

def http_fingerprint(url: str) -> dict:
    """Fingerprint web technology stack via headers and body patterns."""
    import urllib.request, ssl, re
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    techs = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NEXUS-Recon"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            headers = {k: v for k, v in resp.getheaders()}
            body = resp.read().decode("utf-8", errors="ignore")[:50000]
            for h, label in TECH_HEADERS.items():
                if h in headers:
                    techs.append({"source": "header", "tech": f"{label}: {headers[h]}"})
            for pattern, name in BODY_SIGS.items():
                if re.search(pattern, body, re.IGNORECASE):
                    techs.append({"source": "body", "tech": name})
    except Exception as e:
        return {"url": url, "error": str(e), "technologies": []}
    return {"url": url, "technologies": techs, "status": resp.status}


# ── Raw WHOIS lookup via socket (no external deps) ──
def whois_lookup(domain: str) -> dict:
    """Basic WHOIS lookup via socket connection."""
    import socket
    tld = domain.rsplit(".", 1)[-1]
    server = f"whois.nic.{tld}" if tld not in ("com", "net", "org") else f"whois.verisign-grs.com"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((server, 43))
            s.sendall(f"{domain}\r\n".encode())
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            return {"domain": domain, "raw": data.decode("utf-8", errors="ignore")[:2000]}
    except Exception as e:
        return {"domain": domain, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="KERAS__X__HYBRID_2026-AI-COLLEGE-JOBS_x_NLP")
    parser.add_argument("--target", required=True, help="Target path or URL")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    args = parser.parse_args()

    target = args.target
    logger.info(f"[START] {target}")

    results = {}

    try:
        results["dns_recon"] = dns_recon(target)
        logger.info(f"  [dns_recon] OK")
    except Exception as e:
        logger.warning(f"  [dns_recon] SKIP: {e}")

    try:
        results["http_fingerprint"] = http_fingerprint(target)
        logger.info(f"  [http_fingerprint] OK")
    except Exception as e:
        logger.warning(f"  [http_fingerprint] SKIP: {e}")

    report = {
        "agent": "KERAS__X__HYBRID_2026-AI-COLLEGE-JOBS_x_NLP",
        "version": "1.0-gen2",
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] Report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
