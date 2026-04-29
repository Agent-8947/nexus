import json
from pathlib import Path
import argparse

# NEXUS CORE AST RENDERER v1.1 [PORTABLE + DYNAMIC NODE SELECTION]
# FIX [C-01]: All paths relative to __file__
# FIX [C-05]: Removed hardcoded target list -- renders by trait matching or all Gen-0 nodes

DNA_DIR    = Path(__file__).resolve().parent
JSON_PATH  = DNA_DIR / "DNA_04_Synthesis_Core.json"
RENDER_DIR = DNA_DIR / "DNA_12_AST_RENDER"

# AST template library keyed by (domain, role) tuple
RENDERER_MAP = {
    ("osint", "collector"): '''#!/usr/bin/env python3
"""
NEXUS OSINT Collector Agent -- Auto-Synthesized
Generated from DNA traits: domain=osint, role=collector
"""
import asyncio
import aiohttp
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-OSINT")

async def fetch_target(session: aiohttp.ClientSession, target: str) -> dict:
    """Fetch intelligence data for a single target."""
    try:
        async with session.get(f"https://{target}", timeout=aiohttp.ClientTimeout(total=10)) as resp:
            logger.info(f"[+] {target} -> HTTP {resp.status}")
            return {"target": target, "status": resp.status, "size": len(await resp.read())}
    except Exception as e:
        logger.error(f"[!] {target} -> {e}")
        return {"target": target, "error": str(e)}

async def run(targets: list[str]) -> list[dict]:
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_target(session, t) for t in targets]
        results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS OSINT Collector Agent")
    parser.add_argument("--target", required=True, nargs="+", help="Target hosts to scan")
    args = parser.parse_args()
    results = asyncio.run(run(args.target))
    for r in results:
        print(r)
''',

    ("ai", "analyzer"): '''#!/usr/bin/env python3
"""
NEXUS AI Analyzer Agent -- Auto-Synthesized
Generated from DNA traits: domain=ai, role=analyzer
"""
import argparse
import logging
import json

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-AI")

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"[*] PyTorch available. Device: {DEVICE}")
except ImportError:
    DEVICE = "cpu"
    logger.warning("[!] PyTorch not installed. Running in CPU-only mode.")

def analyze_payload(data: str) -> dict:
    """Semantic analysis of input payload."""
    try:
        logger.info(f"[*] Analyzing payload ({len(data)} chars) on {DEVICE}")
        # Placeholder for real model inference
        result = {"input_length": len(data), "device": DEVICE, "confidence": 0.92}
        logger.info(f"[+] Analysis complete: {result}")
        return result
    except Exception as e:
        logger.error(f"[!] Analysis failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS AI Analyzer Agent")
    parser.add_argument("--input", required=True, help="Input data to analyze")
    args = parser.parse_args()
    result = analyze_payload(args.input)
    print(json.dumps(result, indent=2))
''',

    ("security", "orchestrator"): '''#!/usr/bin/env python3
"""
NEXUS Security Orchestrator Agent -- Auto-Synthesized
Generated from DNA traits: domain=security, role=orchestrator, interface=api
"""
import argparse
import logging
import json

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-SEC")

try:
    from fastapi import FastAPI
    import uvicorn
    app = FastAPI(title="NEXUS Security Orchestrator", version="1.0")

    @app.post("/orchestrate")
    async def orchestrate_action(action: str, target: str):
        logger.info(f"[*] Instruction: {action} on {target}")
        return {"status": "dispatched", "target": target, "agents": 3}

    def serve():
        uvicorn.run(app, host="127.0.0.1", port=8000)

except ImportError:
    logger.warning("[!] FastAPI not installed. Running in CLI mode.")
    def serve():
        raise SystemExit("Install fastapi + uvicorn to run API mode.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Security Orchestrator")
    parser.add_argument("--serve", action="store_true", help="Start API server")
    parser.add_argument("--action", default="scan", help="Action to orchestrate")
    parser.add_argument("--target", default="localhost", help="Target host")
    args = parser.parse_args()
    if args.serve:
        serve()
    else:
        logger.info(f"[DRY-RUN] Would orchestrate '{args.action}' -> {args.target}")
''',

    ("infra", "orchestrator"): '''#!/usr/bin/env python3
"""
NEXUS Infra Orchestrator Agent -- Auto-Synthesized
Generated from DNA traits: domain=infra, role=orchestrator
"""
import argparse
import logging
import subprocess
import json

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-INFRA")

def run_health_check(targets: list[str]) -> list[dict]:
    results = []
    for t in targets:
        try:
            proc = subprocess.run(["ping", "-n", "1", t], capture_output=True, text=True, timeout=5)
            up = proc.returncode == 0
            results.append({"host": t, "status": "UP" if up else "DOWN"})
            logger.info(f"[{'UP' if up else 'DOWN'}] {t}")
        except Exception as e:
            results.append({"host": t, "error": str(e)})
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Infra Health Monitor")
    parser.add_argument("--targets", nargs="+", default=["localhost"], help="Hosts to check")
    args = parser.parse_args()
    results = run_health_check(args.targets)
    print(json.dumps(results, indent=2))
''',

    "_generic": '''#!/usr/bin/env python3
"""
NEXUS Generic Utility Agent -- Auto-Synthesized
"""
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-GENERIC")

def main():
    logger.info("[*] NEXUS Generic Agent initialized.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Generic Agent")
    args = parser.parse_args()
    main()
'''
}


def select_template(traits: dict) -> str:
    """Select the best matching template for given DNA traits."""
    domain = traits.get("domain", "")
    role   = traits.get("role", "")

    key = (domain, role)
    if key in RENDERER_MAP:
        return RENDERER_MAP[key]

    # Fallback: match on domain only
    for (d, r), code in RENDERER_MAP.items():
        if d == domain and d != "_generic":
            return code

    return RENDERER_MAP["_generic"]


def render_node(node: dict) -> bool:
    """Render a single DNA node to Python code."""
    node_id = node['node_id']
    traits  = node['evolution_matrix']['traits_fixed']

    template = select_template(traits)

    out_file = RENDER_DIR / f"{node_id}_synthesized_agent.py"
    out_file.parent.mkdir(exist_ok=True, parents=True)
    out_file.write_text(template.strip(), encoding='utf-8')
    print(f"  [+] {node_id:30s} -> {out_file.name}")
    return True


def render_all(node_ids: list | None = None, generation: int = 0, max_nodes: int = 0):
    """Render nodes from DNA_04. Optionally filter by node_id list or limit count."""
    if not JSON_PATH.exists():
        print(f"[!] DNA Core missing. Run DNA_03 first.\n    Expected: {JSON_PATH}")
        return 0

    dna = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    all_nodes = dna.get("NODES", [])

    # Filter by generation
    targets = [n for n in all_nodes
               if n["evolution_matrix"]["lineage"]["generation"] == generation]

    if node_ids:
        targets = [n for n in targets if n["node_id"] in node_ids]

    if max_nodes > 0:
        targets = targets[:max_nodes]

    print(f"[*] AST Rendering {len(targets)} Gen-{generation} nodes...")
    print(f"    Output: {RENDER_DIR}\n")

    rendered = 0
    for node in targets:
        if render_node(node):
            rendered += 1

    print(f"\n[AST RENDER COMPLETE] {rendered}/{len(targets)} nodes rendered.")
    return rendered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS AST Renderer v1.1")
    parser.add_argument("--node-id",  nargs="+", help="Specific node IDs to render")
    parser.add_argument("--gen",      type=int, default=0, help="Generation to render (default: 0)")
    parser.add_argument("--max",      type=int, default=0, help="Max nodes to render (0 = all)")
    args = parser.parse_args()

    render_all(
        node_ids=args.node_id,
        generation=args.gen,
        max_nodes=args.max
    )
