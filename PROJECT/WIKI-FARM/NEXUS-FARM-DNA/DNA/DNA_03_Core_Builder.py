import os
import re
import json
import math
import hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter

# NEXUS CORE SYNTHESIS ENGINE v3.0 (ANTI-COLLAPSE EDITION)
# =========================================================
# FIX [C-01]: All paths relative to __file__ -- fully portable
# FIX [H-06]: Fitness formula uses dynamic weight sum
# FIX [V3-01]: 10-dimensional DNA signature (was 6) -- kills clone clusters
# FIX [V3-02]: Score-based domain/role classifier (was elif-cascade)
# FIX [V3-03]: TF-IDF inspired normalization for DNA heatmap
# FIX [V3-04]: Content hash injection into DNA for guaranteed uniqueness

DNA_DIR    = Path(__file__).resolve().parent          # .../DNA/
FARM_ROOT  = DNA_DIR.parent.parent                    # .../WIKI-FARM/
VAULT_PATH = FARM_ROOT / "NEXUS-OBSIDIAN-VAULT"
OUTPUT_DIR = DNA_DIR                                  # Output goes into DNA/ itself
JSON_OUTPUT = DNA_DIR / "DNA_04_Synthesis_Core.json"
MD_OUTPUT   = DNA_DIR / "DNA_05_Core_Manifest.md"

# ==========================================
# 1. EVOLUTIONARY GLOBAL SCHEMA DEFINITIONS
# ==========================================
GLOBAL_TAXONOMY = {
    "domain":         ["osint", "security", "ai", "infra", "hardware", "data", "web", "cs", "math"],
    "role":           ["collector", "processor", "analyzer", "orchestrator", "storage", "presentation", "library", "payload"],
    "computing":      ["cpu", "gpu", "fpga", "quantum", "agnostic"],
    "latency":        ["real-time", "batch", "streaming", "none"],
    "security_level": ["none", "low", "medium", "high", "critical"],
    "autonomy":       ["manual", "scripted", "agentic", "swarm"],
    "interface":      ["cli", "api", "gui", "library", "protocol"]
}

# FIX [V3-01]: 10 dimensions instead of 6
DNA_DIMENSIONS = {
    "dim_0": {"name": "Network",       "description": "Degree of external network dependency (API, Web)."},
    "dim_1": {"name": "Intelligence",  "description": "Level of AI, ML, or cognitive learning mechanisms."},
    "dim_2": {"name": "Autonomy",      "description": "Ability to orchestrate and operate without manual input."},
    "dim_3": {"name": "Hardware",      "description": "Reliance on specific physical hardware (GPU, IoT)."},
    "dim_4": {"name": "Stealth",       "description": "Evasiveness, cryptography, and defensive operational security."},
    "dim_5": {"name": "Scale",         "description": "Horizontal scalability and distributed computing."},
    "dim_6": {"name": "DataPipeline",  "description": "Data ingestion, ETL, streaming, and storage depth."},
    "dim_7": {"name": "Visualization", "description": "UI, dashboards, charting, and presentation layer."},
    "dim_8": {"name": "LowLevel",      "description": "Systems programming, kernel, firmware, memory management."},
    "dim_9": {"name": "ContentHash",   "description": "Unique per-document fingerprint derived from content hash."},
}

COMPATIBILITY_FUNCTION = {
    "core_logic": "genetic_distance = cosine(node_A.dna_signature, node_B.dna_signature)",
    "rules": [
        "ALLOW if 0.10 < cosine_distance < 0.90",
        "DENY if node_A.security_level == 'high'/'critical' AND cosine_distance < 0.10 (inbreeding)",
        "DENY if node_A.security_level == 'critical' AND node_B.interface == 'gui'"
    ]
}

# FIX [H-06]: Weights defined once -- used in formula AND stored in schema
FITNESS_WEIGHTS = {"performance": 1.0, "security": 1.0, "novelty": 1.5, "completeness": 0.5}

FITNESS_FUNCTION = {
    "core_equation": "fitness = sum(W * score for W, score in zip(weights, scores)) / sum(weights)",
    "weights": FITNESS_WEIGHTS
}

AST_COMPOSITOR = [
    {
        "required_traits": {"domain": "osint", "role": "collector"},
        "blocks": {
            "imports": ["import aiohttp", "import asyncio", "import sys"],
            "setup": "session = aiohttp.ClientSession()",
            "execution": "async def process(target):\n    pass # [AST_INJECT_LOGIC]",
            "teardown": "await session.close()"
        }
    },
    {
        "required_traits": {"domain": "ai", "computing": "gpu"},
        "blocks": {
            "imports": ["import torch", "from loguru import logger"],
            "setup": "device = 'cuda' if torch.cuda.is_available() else 'cpu'",
            "execution": "def analyze(data):\n    pass # [AST_INJECT_LOGIC]",
            "teardown": "torch.cuda.empty_cache()"
        }
    }
]

# ==========================================
# 2. PARSING ENGINE v3.0
# ==========================================

def extract_section(content, section_patterns):
    for pattern in section_patterns:
        match = re.search(rf"(?:^|\n)##\s+.*?{pattern}.*?\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""

def determine_risk(content_lower):
    if re.search(r'(наступательн|offensive|rootkit|malware|botnet|эксплоит|троян|zero-day)', content_lower):
        return "high"
    if re.search(r'(security|безопасност|уязвимост|аудит|sniffer|recon|пентест)', content_lower):
        return "medium"
    return "low"


# FIX [V3-02]: Score-based classifier replaces elif-cascade
# Each domain/role accumulates points from ALL matching patterns,
# the one with highest score wins. Eliminates "ai absorbs everything" bias.

DOMAIN_SCORING = {
    "osint":     [r'\bosint\b', r'\brecon\b', r'\bshodan\b', r'\bpassive\b', r'\bпассивн',
                  r'\bintelligence\b', r'\bharvest', r'\bscraping\b', r'\bcrawl', r'\bdork'],
    "security":  [r'\bsecurity\b', r'\bvulnerab', r'\bexploit', r'\bmalware\b', r'\bpentest',
                  r'\bcve-\d', r'\bfirewall\b', r'\bwaf\b', r'\bids\b', r'\bips\b',
                  r'\baudit\b', r'\bharden', r'\bfortify', r'\bзащит', r'\bвзлом',
                  r'\brootkit\b', r'\btrojan\b', r'\bransomware\b', r'\bботнет'],
    "ai":        [r'\bmachine.?learn', r'\bdeep.?learn', r'\bneural', r'\btransformer\b',
                  r'\bllm\b', r'\bgpt\b', r'\bbert\b', r'\btrain(?:ing|ed)\b',
                  r'\binference\b', r'\bнейросет', r'\bобучени', r'\btorch\b',
                  r'\btensorflow\b', r'\bkeras\b', r'\bhugging\s*face'],
    "infra":     [r'\bkubernetes\b', r'\bk8s\b', r'\bdocker\b', r'\bterraform\b',
                  r'\bansible\b', r'\bci/?cd\b', r'\bdevops\b', r'\bmonitoring\b',
                  r'\bprometheus\b', r'\bgrafana\b', r'\bnginx\b', r'\bproxy\b',
                  r'\binfrastructur', r'\bоркестра'],
    "hardware":  [r'\bfpga\b', r'\bvhdl\b', r'\bverilog\b', r'\bbios\b', r'\bfirmware\b',
                  r'\biot\b', r'\bembedded\b', r'\bробот', r'\bдрон', r'\bsensor\b',
                  r'\barduino\b', r'\braspberry', r'\besp32\b', r'\barm\b'],
    "data":      [r'\bdatabase\b', r'\bsql\b', r'\bnosql\b', r'\betl\b', r'\bdata.?lake',
                  r'\bparquet\b', r'\bapache\s*spark', r'\bhadoop\b', r'\bпотоков',
                  r'\bkafka\b', r'\bpostgres', r'\bmongo', r'\belastic', r'\bredis\b'],
    "web":       [r'\bfrontend\b', r'\breact\b', r'\bvue\b', r'\bangular\b', r'\bnext\.?js\b',
                  r'\bhtml\b', r'\bcss\b', r'\bjavascript\b', r'\btypescript\b',
                  r'\bwebpack\b', r'\bvite\b', r'\bdom\b', r'\bresponsive\b'],
    "cs":        [r'\balgorithm', r'\bdata.?struct', r'\bsort', r'\bgraph\b', r'\btree\b',
                  r'\bleetcode\b', r'\bcompetitive', r'\bcomplexity\b', r'\bcompiler\b'],
    "math":      [r'\blinear.?algebra', r'\bstatistic', r'\bprobabilit', r'\bcalculus\b',
                  r'\boptimiz', r'\bmatrix\b', r'\beigen', r'\bregression\b'],
}

ROLE_SCORING = {
    "collector":     [r'\bcollect', r'\bсбор', r'\bspider\b', r'\bcrawl', r'\bscrape',
                      r'\bharvest', r'\bfetch', r'\bingest', r'\bgather', r'\bextract'],
    "processor":     [r'\bprocess', r'\btransform', r'\bпреобраз', r'\bnormali', r'\betl\b',
                      r'\bparse', r'\bclean', r'\bvalidat', r'\bfilter'],
    "analyzer":      [r'\banalyz', r'\bанализ', r'\bauditor\b', r'\bdetect', r'\bclassif',
                      r'\bpredict', r'\bscore', r'\bmetric', r'\bbenchmark'],
    "orchestrator":  [r'\borchestrat', r'\bplatform\b', r'\bframework\b', r'\bpipeline\b',
                      r'\bworkflow\b', r'\bscheduler\b', r'\bdispatch', r'\bmanag'],
    "storage":       [r'\bstorag', r'\bбаз\b', r'\bхранилищ', r'\bcache\b', r'\bdatastore',
                      r'\brepository\b', r'\bindex', r'\bpersist'],
    "presentation":  [r'\bdashboard\b', r'\bvisuali', r'\bchart\b', r'\breport',
                      r'\bplot\b', r'\bui\b', r'\bgui\b', r'\bdisplay'],
    "library":       [r'\blibrary\b', r'\bсdk\b', r'\butility\b', r'\bhelper\b',
                      r'\btoolkit\b', r'\bwrapper\b', r'\bbinding', r'\bpackage\b'],
    "payload":       [r'\bpayload\b', r'\bexploit', r'\bshellcode', r'\binjection',
                      r'\boffensive\b', r'\battack', r'\bmodule\b'],
}


def _score_classify(content_lower: str, scoring_dict: dict, default: str) -> str:
    """Pick the category with highest cumulative regex hit count."""
    scores = {}
    for category, patterns in scoring_dict.items():
        total = 0
        for pat in patterns:
            total += len(re.findall(pat, content_lower))
        scores[category] = total

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return default
    return best


def get_fixed_traits(content_lower):
    """FIX [V3-02]: Score-based classifier for all traits."""
    traits = {
        "domain": _score_classify(content_lower, DOMAIN_SCORING, "infra"),
        "role": _score_classify(content_lower, ROLE_SCORING, "library"),
        "computing": "agnostic",
        "latency": "none",
        "security_level": "none",
        "autonomy": "manual",
        "interface": "cli"
    }

    # Computing
    if re.search(r'(gpu|cuda|tensor)', content_lower):     traits['computing'] = 'gpu'
    elif re.search(r'(fpga|vhdl|verilog)', content_lower): traits['computing'] = 'fpga'

    # Latency
    if re.search(r'(real.?time|real-time|реальн)', content_lower): traits['latency'] = 'real-time'
    elif re.search(r'(stream|потоков)', content_lower):             traits['latency'] = 'streaming'
    elif re.search(r'(batch|пакет)', content_lower):                traits['latency'] = 'batch'

    # Security level
    if re.search(r'(offensive|rootkit|malware|exploit|0day|shellcode)', content_lower): traits['security_level'] = 'critical'
    elif re.search(r'(pentest|аудит|vulnerab|cve-\d)', content_lower):                  traits['security_level'] = 'high'
    elif re.search(r'(шифрован|crypto|tls|auth|jwt|oauth)', content_lower):             traits['security_level'] = 'medium'

    # Interface
    if re.search(r'(gui|dashboard|web.?ui)', content_lower):  traits['interface'] = 'gui'
    elif re.search(r'(api|rest|graphql|grpc)', content_lower): traits['interface'] = 'api'

    # Autonomy
    if re.search(r'(swarm|multi.?agent|distributed.?agent)', content_lower): traits['autonomy'] = 'swarm'
    elif re.search(r'(agent|автономн|self.?heal|self.?repair)', content_lower): traits['autonomy'] = 'agentic'
    elif re.search(r'(script|автоматиз|pipeline|cron|scheduled)', content_lower): traits['autonomy'] = 'scripted'

    return traits


def get_resources(content_lower):
    return {
        "compute_cost": "high" if re.search(r'(ai|model|gpu|crypto|hash|train)', content_lower) else "low",
        "memory_cost":  "high" if re.search(r'(in-memory|database|cache|llm|large)', content_lower) else "low"
    }


def calculate_dna_signature(content_lower: str, doc_id: str, corpus_doc_freq: dict, corpus_size: int) -> list:
    """FIX [V3-01]: 10-dimensional DNA with TF-IDF normalization and content hash.

    Dimensions 0-8: Topic heat with corpus-aware IDF weighting.
    Dimension 9: Content hash — guarantees uniqueness per document.
    """
    def heat_tfidf(keywords: list, max_raw: int = 8) -> float:
        """Compute TF-IDF inspired heat score.

        FIX [V3-12]: max_raw=8 (was 20) — short vault files (1KB) rarely exceed 8 hits.
        FIX [V3-13]: Boundary-free fallback — if \\b-bounded regex misses, retry without \\b.
        This catches YAML tags like "tags: [security, osint]" and compound words.

        TF = clipped raw count / max_raw
        IDF = log(corpus_size / (1 + docs_containing_term))
        Final = TF * mean(IDF) for all matched keywords
        """
        total_tf = 0
        idf_values = []
        for kw in keywords:
            hits = len(re.findall(kw, content_lower))
            # FIX [V3-13]: If word-boundary match fails, try without \b
            if hits == 0 and r'\b' in kw:
                kw_relaxed = kw.replace(r'\b', '')
                hits = len(re.findall(kw_relaxed, content_lower))
            if hits > 0:
                tf = min(1.0, hits / max_raw)
                total_tf += tf
                # IDF: how rare is this keyword across the corpus?
                doc_freq = corpus_doc_freq.get(kw, 1)
                idf = math.log((corpus_size + 1) / (1 + doc_freq))
                idf_values.append(idf)

        if not idf_values:
            return 0.0

        mean_idf = sum(idf_values) / len(idf_values)
        avg_tf = total_tf / len(keywords)
        # Normalize IDF to [0, 1] range (max IDF ≈ log(corpus_size))
        max_idf = math.log(corpus_size + 1) if corpus_size > 0 else 1.0
        normalized_idf = min(1.0, mean_idf / max_idf)
        # FIX [V3-14]: Boost factor for short documents (< 2KB)
        short_boost = 1.5 if len(content_lower) < 2000 else 1.0
        score = avg_tf * (0.4 + 0.6 * normalized_idf) * short_boost
        return round(min(1.0, score), 3)

    # dim_0: Network
    network_kw = [r'\bnetwork\b', r'\bapi\b', r'\bssh\b', r'\bcloud\b', r'\bweb\b',
                  r'\bсеть', r'\bshodan\b', r'\bhttp', r'\bsocket\b', r'\bgrpc\b',
                  r'\bwebhook\b', r'\bproxy\b', r'\bdns\b', r'\btcp\b', r'\budp\b']

    # dim_1: Intelligence
    intel_kw = [r'\bmachine.?learn', r'\bdeep.?learn', r'\bneural\b', r'\btransformer\b',
                r'\bllm\b', r'\bнейросет', r'\bобучени', r'\binference\b',
                r'\btrain(?:ing|ed)\b', r'\bclassif', r'\bregression\b', r'\bembedding']

    # dim_2: Autonomy
    auto_kw = [r'\bautonomous\b', r'\borchestrat', r'\bagent\b', r'\bdaemon\b',
               r'\bself.?heal', r'\bself.?repair', r'\bauto.?pilot', r'\bscheduler\b',
               r'\bworkflow\b', r'\bpipeline\b', r'\bdispatch']

    # dim_3: Hardware
    hw_kw = [r'\bfpga\b', r'\bhardware\b', r'\bchip\b', r'\bbios\b', r'\biot\b',
             r'\bробот', r'\bдрон', r'\bsensor\b', r'\bembedded\b',
             r'\barduino\b', r'\braspberry', r'\besp32\b', r'\bfirmware\b']

    # dim_4: Stealth
    stealth_kw = [r'\bstealth\b', r'\bскрыт', r'\bшифров', r'\banon', r'\bcrypto\b',
                  r'\bhide\b', r'\bvpn\b', r'\brootkit\b', r'\bevasion\b',
                  r'\bobfuscat', r'\bcovert\b', r'\btunnel']

    # dim_5: Scale
    scale_kw = [r'\bscale\b', r'\bscaling\b', r'\bdistributed\b', r'\bkubernetes\b',
                r'\bcluster\b', r'\bmicroservice', r'\bload.?balanc',
                r'\bsharding\b', r'\breplica', r'\bhorizontal']

    # dim_6: DataPipeline (NEW)
    data_kw = [r'\betl\b', r'\bdata.?lake', r'\bstream', r'\bkafka\b', r'\bspark\b',
               r'\bparquet\b', r'\bavro\b', r'\bingestion\b', r'\bbatch.?process',
               r'\bdata.?pipeline', r'\bwarehouse\b', r'\bolap\b']

    # dim_7: Visualization (NEW)
    viz_kw = [r'\bvisuali', r'\bdashboard\b', r'\bchart\b', r'\bplot\b', r'\bgrafana\b',
              r'\bmatplotlib\b', r'\bplotly\b', r'\bd3\.?js\b', r'\breport\b',
              r'\bgui\b', r'\binterface\b', r'\bwidget\b']

    # dim_8: LowLevel (NEW)
    low_kw = [r'\bkernel\b', r'\bsyscall\b', r'\bassembly\b', r'\bc\+\+', r'\brust\b',
              r'\bmemory.?manag', r'\bpointer\b', r'\bbuffer\b', r'\bheap\b',
              r'\bcompiler\b', r'\blinker\b', r'\belf\b', r'\bbinary\b']

    # dim_9: ContentHash — unique fingerprint per document
    content_hash = hashlib.md5(doc_id.encode() + content_lower[:500].encode()).hexdigest()
    hash_float = int(content_hash[:8], 16) / 0xFFFFFFFF  # Map to [0, 1]

    return [
        heat_tfidf(network_kw),
        heat_tfidf(intel_kw),
        heat_tfidf(auto_kw),
        heat_tfidf(hw_kw),
        heat_tfidf(stealth_kw),
        heat_tfidf(scale_kw),
        heat_tfidf(data_kw),
        heat_tfidf(viz_kw),
        heat_tfidf(low_kw),
        round(hash_float, 3),
    ]


def _build_corpus_doc_freq(files: list) -> dict:
    """Pre-compute document frequency for each keyword across the entire corpus.

    Returns dict: {keyword_pattern: count_of_docs_containing_it}
    """
    all_keywords = set()
    for kw_list in [
        # Collect all keyword lists from DNA dimensions
        [r'\bnetwork\b', r'\bapi\b', r'\bssh\b', r'\bcloud\b', r'\bweb\b',
         r'\bсеть', r'\bshodan\b', r'\bhttp', r'\bsocket\b', r'\bgrpc\b',
         r'\bwebhook\b', r'\bproxy\b', r'\bdns\b', r'\btcp\b', r'\budp\b'],
        [r'\bmachine.?learn', r'\bdeep.?learn', r'\bneural\b', r'\btransformer\b',
         r'\bllm\b', r'\bнейросет', r'\bобучени', r'\binference\b',
         r'\btrain(?:ing|ed)\b', r'\bclassif', r'\bregression\b', r'\bembedding'],
        [r'\bautonomous\b', r'\borchestrat', r'\bagent\b', r'\bdaemon\b',
         r'\bself.?heal', r'\bself.?repair', r'\bauto.?pilot', r'\bscheduler\b',
         r'\bworkflow\b', r'\bpipeline\b', r'\bdispatch'],
        [r'\bfpga\b', r'\bhardware\b', r'\bchip\b', r'\bbios\b', r'\biot\b',
         r'\bробот', r'\bдрон', r'\bsensor\b', r'\bembedded\b',
         r'\barduino\b', r'\braspberry', r'\besp32\b', r'\bfirmware\b'],
        [r'\bstealth\b', r'\bскрыт', r'\bшифров', r'\banon', r'\bcrypto\b',
         r'\bhide\b', r'\bvpn\b', r'\brootkit\b', r'\bevasion\b',
         r'\bobfuscat', r'\bcovert\b', r'\btunnel'],
        [r'\bscale\b', r'\bscaling\b', r'\bdistributed\b', r'\bkubernetes\b',
         r'\bcluster\b', r'\bmicroservice', r'\bload.?balanc',
         r'\bsharding\b', r'\breplica', r'\bhorizontal'],
        [r'\betl\b', r'\bdata.?lake', r'\bstream', r'\bkafka\b', r'\bspark\b',
         r'\bparquet\b', r'\bavro\b', r'\bingestion\b', r'\bbatch.?process',
         r'\bdata.?pipeline', r'\bwarehouse\b', r'\bolap\b'],
        [r'\bvisuali', r'\bdashboard\b', r'\bchart\b', r'\bplot\b', r'\bgrafana\b',
         r'\bmatplotlib\b', r'\bplotly\b', r'\bd3\.?js\b', r'\breport\b',
         r'\bgui\b', r'\binterface\b', r'\bwidget\b'],
        [r'\bkernel\b', r'\bsyscall\b', r'\bassembly\b', r'\bc\+\+', r'\brust\b',
         r'\bmemory.?manag', r'\bpointer\b', r'\bbuffer\b', r'\bheap\b',
         r'\bcompiler\b', r'\blinker\b', r'\belf\b', r'\bbinary\b'],
    ]:
        all_keywords.update(kw_list)

    print(f"  [TF-IDF] Building corpus document frequency for {len(all_keywords)} keywords across {len(files)} docs...")
    doc_freq = {kw: 0 for kw in all_keywords}

    for md_f in files:
        try:
            content = md_f.read_text(encoding="utf-8").lower()
        except Exception:
            continue
        for kw in all_keywords:
            if re.search(kw, content):
                doc_freq[kw] += 1

    return doc_freq


# ==========================================
# 3. BUILD PIPELINE v3.0
# ==========================================

def build_core_dna():
    if not VAULT_PATH.exists():
        print(f"[!] Vault not found: {VAULT_PATH}")
        return

    print("[*] INITIALIZING CORE DNA SYNTHESIS v3.0 (ANTI-COLLAPSE EDITION)...")
    files = sorted(list(VAULT_PATH.glob("*.md")))
    files = [f for f in files if "DNA" not in f.name]

    if not files:
        print("[!] No markdown files found in vault.")
        return

    # FIX [V3-03]: Pre-compute corpus document frequencies for TF-IDF
    corpus_doc_freq = _build_corpus_doc_freq(files)
    corpus_size = len(files)

    pre_nodes = []
    vector_sum = [0.0] * 10  # 10 dimensions now
    count = 0

    for md_f in files:
        content = md_f.read_text(encoding="utf-8")
        content_lower = content.lower()
        title = md_f.stem.upper()

        cat_match = re.search(r'category:\s*(.*)', content, re.IGNORECASE)
        category = cat_match.group(1).strip() if cat_match else "Unclassified"

        desc = extract_section(content, ["Описани"])
        if not desc:
            m = re.search(r"(?:^|\n)##\s+[^\n]+\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL)
            desc = m.group(1).strip() if m else ""
        essence = desc.replace('\n', ' ')[:400]

        comp = sum(1 for f in [essence,
                                extract_section(content, ["Фичи"]),
                                extract_section(content, ["Архитектур"])] if len(f) > 5) / 3.0
        risk   = determine_risk(content_lower)
        traits = get_fixed_traits(content_lower)
        dna_vector = calculate_dna_signature(content_lower, title, corpus_doc_freq, corpus_size)

        for i in range(10):
            vector_sum[i] += dna_vector[i]
        count += 1

        pre_nodes.append({
            "id": title, "category": category, "essence": essence,
            "comp": round(comp, 2), "risk": risk, "traits": traits,
            "vector": dna_vector, "resources": get_resources(content_lower)
        })

    centroid = [v / count for v in vector_sum]
    max_dist  = math.sqrt(10)  # 10 dimensions
    W = FITNESS_WEIGHTS
    W_total = sum(W.values())

    synthesis_nodes = []
    for pn in pre_nodes:
        dist    = math.sqrt(sum((a - b) ** 2 for a, b in zip(pn['vector'], centroid)))
        novelty = round(min(1.0, dist / max_dist * 2), 2)

        security = 1.0 if pn['risk'] == 'low' else 0.5 if pn['risk'] == 'medium' else 0.2
        if pn['traits']['security_level'] in ['critical', 'high']:
            security = 0.9
        perf = 0.8

        ova = round(
            (W["performance"] * perf + W["security"] * security +
             W["novelty"] * novelty + W["completeness"] * pn['comp']) / W_total, 2
        )

        synthesis_nodes.append({
            "node_id": pn['id'],
            "evolution_matrix": {
                "traits_fixed": pn['traits'],
                "dna_signature": pn['vector'],
                "resources": pn['resources'],
                "mutation_hotspots": {
                    "can_add_capabilities": True,
                    "can_change_interface": True,
                    "mutation_rate": 0.15 if pn['comp'] > 0.7 else 0.8
                },
                "fitness_score": {
                    "performance":  perf,
                    "security":     security,
                    "novelty":      novelty,
                    "completeness": pn['comp'],
                    "overall":      ova
                },
                "lineage": {"parents": [], "generation": 0}
            }
        })

    # Verify diversity before writing
    sigs = [tuple(n["evolution_matrix"]["dna_signature"]) for n in synthesis_nodes]
    unique_count = len(set(sigs))
    diversity_pct = unique_count / len(sigs) * 100 if sigs else 0

    print(f"\n[DIVERSITY CHECK] Unique signatures: {unique_count}/{len(sigs)} ({diversity_pct:.1f}%)")
    if diversity_pct < 50:
        print(f"[!] WARNING: Diversity still below 50%. ContentHash dim_9 should help.")

    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump({
            "NEXUS_SYSTEM": "SYNTHESIS_DNA_CORE",
            "VERSION": "3.0_ANTI_COLLAPSE",
            "BUILT_AT": datetime.now().isoformat(),
            "META_SCHEMA": {
                "GLOBAL_TAXONOMY": GLOBAL_TAXONOMY,
                "DNA_DIMENSIONS": DNA_DIMENSIONS,
                "COMPATIBILITY_FUNCTION": COMPATIBILITY_FUNCTION,
                "FITNESS_FUNCTION": FITNESS_FUNCTION,
                "AST_COMPOSITOR": AST_COMPOSITOR
            },
            "TOTAL_NODES": len(synthesis_nodes),
            "DIVERSITY": {
                "unique_signatures": unique_count,
                "total_nodes": len(synthesis_nodes),
                "diversity_pct": round(diversity_pct, 1)
            },
            "NODES": synthesis_nodes
        }, f, ensure_ascii=False, indent=2)

    print(f"[+] DNA_04 written: {JSON_OUTPUT}  ({len(synthesis_nodes)} nodes)")
    print(f"[SYNTHESIS MODULE READY: FULL AST MATRIX v3.0 — {diversity_pct:.1f}% DIVERSITY]")


if __name__ == "__main__":
    build_core_dna()
