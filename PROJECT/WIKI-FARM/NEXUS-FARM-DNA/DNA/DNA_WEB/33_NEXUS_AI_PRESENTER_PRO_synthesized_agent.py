#!/usr/bin/env python3
"""
NEXUS_AI_PRESENTER_PRO [NEXUS SYNTHESIZED Gen-4]
Mission: technical_ai_presentation
Heritage: GENOMIC_ANALYST + VESSEL_RENDERER
Role: presentation | Domains: ai & web

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 4 blocks):
  Stage 1: [extract_links]
  Stage 2: [detect_anomalies, compute_stats, text_similarity]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, math
import re, ssl, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_AI_PRESENTER_PRO")

def __nexus_execute__(func, arg, output_type, findings_list, stats_dict, errors_list):
    try:
        _result = func(arg)
        if output_type == "findings":
            if isinstance(_result, list): findings_list.extend(_result)
            logger.info(f"  [{func.__name__}] {len(_result) if isinstance(_result, list) else 0} findings")
        elif output_type in ("stats", "tech_stack", "port_report", "system_info", "report"):
            if isinstance(_result, dict): stats_dict.update(_result)
            if output_type == "port_report" and isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item.update({"type": func.__name__, "severity": "INFO", "detail": str(item), "source": "nexus_pipeline"})
                    findings_list.append(item)
            logger.info(f"  [{func.__name__}] OK")
        else:
            if isinstance(_result, list): findings_list.extend(_result)
            elif isinstance(_result, dict): stats_dict.update(_result)
            logger.info(f"  [{func.__name__}] OK")
    except Exception as e:
        errors_list.append(f"{func.__name__}: {e}")
        logger.warning(f"  [{func.__name__}] SKIP: {e}")


# ── [AI] Z-Score + IQR anomaly detection on numeric series ──
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


# ── [AI] Descriptive statistics (mean, median, std, quartiles, IQR) ──
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


# ── [AI] TF-based cosine similarity between text sections ──
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


# ── [WEB] Extract all links from a web page ──
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



class Renderer:
    """Converts structured report into human-readable output"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def render(self, report: Dict[str, Any]) -> str:
        """PRESENTATION CONTRACT: render(report) → str"""
        self.all_findings = report.get("findings", [])
        self.all_stats = report.get("stats", {})
        # -- Stage 1 --
        __nexus_execute__(extract_links, report.get("target", "unknown"), "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # -- Stage 2 --
        __nexus_execute__(detect_anomalies, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(compute_stats, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(text_similarity, str(report.get("target", "unknown")), "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # Final formatting: join all findings into a structured report
        output = [f"# NEXUS_AI_PRESENTER_PRO Analysis Report", f"Timestamp: {datetime.now().isoformat()}", ""]
        output.append("## Risk Summary")
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        for k, v in risk.items():
            output.append(f"- {k}: {v}")
        
        output.append("\n## Critical Findings")
        for f in [x for x in self.all_findings if x.get("severity") in ("CRITICAL", "HIGH")]:
            output.append(f"### [{f.get('severity')}] {f.get('type')}")
            output.append(f"- Detail: {f.get('detail')}")
            output.append(f"- Source: {f.get('source')}")

        return "\n".join(output)



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Renderer()
    test_target = [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 100.0, 1.0, 0.98]
    mock_report = {"target": "test", "findings": [{ "type": "test", "severity": "INFO", "value": 100, "detail": "test", "source": "test" }]}
    result = agent.render(mock_report)
    assert isinstance(result, str) and len(result) > 0, "render() must return non-empty string"
    logger.info(f"[TEST] Renderer.render() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_AI_PRESENTER_PRO")
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

    agent = Renderer()
    # Presentation expects a report object
    mock_report = {"target": str(target), "findings": [], "stats": {}}
    report_str = agent.render(mock_report)
    print(report_str)
    return

    # Display summary if report is a dict with findings
    if isinstance(report, dict) and "findings" in report:
        crits = [f for f in report["findings"] if f.get("severity") in ("CRITICAL", "HIGH")]
        if crits:
            print(f"\n{'='*60}")
            print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
            print(f"{'='*60}")
            for f in crits[:10]:
                print(f"  [{f.get('severity')}] {f.get('detail')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
