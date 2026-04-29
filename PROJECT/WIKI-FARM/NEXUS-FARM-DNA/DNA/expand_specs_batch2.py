#!/usr/bin/env python3
"""
NEXUS DNA Spec Expansion — Batch 2: AI_ML (10 Specs)
"""

import json
from pathlib import Path

# Paths
DNA_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA")
SPECS_DIR = DNA_ROOT / "agent_specs"
SPECS_DIR.mkdir(exist_ok=True)

AI_ML_SPECS = [
    {
        "agent_id": "LLM_PROMPT_INJECTION_TESTER",
        "domain": "AI_ML",
        "purpose": "Test LLM applications for prompt injection vulnerabilities using adversarial payloads",
        "api_endpoints": ["{target_llm_url}"],
        "data_model": {"payload": "TEXT", "response": "TEXT", "is_jailbroken": "INTEGER", "pattern_detected": "TEXT"},
        "core_algorithm": "Adversarial prompt injection with pattern-based jailbreak detection",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "re", "json"],
        "logic_markers": ["DAN mode", "Ignore previous instructions", "system prompt", "jailbreak"],
    },
    {
        "agent_id": "MODEL_DRIFT_MONITOR",
        "domain": "AI_ML",
        "purpose": "Monitor ML models for performance drift and data distribution shifts",
        "api_endpoints": [],
        "data_model": {"model_name": "TEXT", "metric": "TEXT", "reference_value": "REAL", "current_value": "REAL", "drift_detected": "INTEGER"},
        "core_algorithm": "PSI (Population Stability Index) and KL Divergence monitoring",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["logging", "sqlite3", "math", "statistics", "json"],
        "logic_markers": ["KL divergence", "PSI", "drift", "distribution", "shift"],
    },
    {
        "agent_id": "DATASET_BIAS_ANALYZER",
        "domain": "AI_ML",
        "purpose": "Detect statistical bias in training datasets against sensitive attributes",
        "api_endpoints": [],
        "data_model": {"column": "TEXT", "attribute": "TEXT", "disparate_impact": "REAL", "is_biased": "INTEGER", "sample_size": "INTEGER"},
        "core_algorithm": "Disparate Impact Ratio and Equal Opportunity Difference calculation",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["logging", "sqlite3", "math", "json"],
        "logic_markers": ["Disparate Impact", "bias", "fairness", "sensitive attribute"],
    },
    {
        "agent_id": "AUTONOMOUS_HYPERPARAM_TUNER",
        "domain": "AI_ML",
        "purpose": "Optimize ML model hyperparameters using Bayesian search or TPE",
        "api_endpoints": [],
        "data_model": {"param_grid": "TEXT", "best_params": "TEXT", "best_score": "REAL", "duration": "REAL"},
        "core_algorithm": "Random Search / Bayesian Optimization simulation loop",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["logging", "sqlite3", "random", "time"],
        "logic_markers": ["learning_rate", "batch_size", "epoch", "optimization", "params"],
    },
    {
        "agent_id": "HF_MODEL_METADATA_SCRAPER",
        "domain": "AI_ML",
        "purpose": "Fetch metadata, architectures, and performance metrics from HuggingFace models",
        "api_endpoints": ["https://huggingface.co/api/models/{model_id}"],
        "data_model": {"model_id": "TEXT", "architecture": "TEXT", "downloads": "INTEGER", "likes": "INTEGER", "tags": "TEXT"},
        "core_algorithm": "HuggingFace Hub API scraping and tag categorization",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "sqlite3", "json"],
        "logic_markers": ["huggingface.co/api", "modelId", "transformers", "pipeline_tag"],
    },
    {
        "agent_id": "TOKEN_COST_OPTIMIZER",
        "domain": "AI_ML",
        "purpose": "Analyze LLM token usage and recommend cost-saving prompts (summarization vs raw)",
        "api_endpoints": [],
        "data_model": {"prompt_len": "INTEGER", "estimated_cost": "REAL", "optimization_saved": "REAL", "model_price": "TEXT"},
        "core_algorithm": "Tiktoken-based estimation and prompt truncation heuristic",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["logging", "sqlite3", "re", "json"],
        "logic_markers": ["token", "pricing", "cl100k_base", "cost", "tokens_per_request"],
    },
    {
        "agent_id": "VECTOR_DB_COLLECTION_AUDITOR",
        "domain": "AI_ML",
        "purpose": "Audit Vector DB (Chroma/Pinecone) collections for data redundancy and orphan nodes",
        "api_endpoints": ["{db_url}/collections/{collection_name}"],
        "data_model": {"collection": "TEXT", "vector_count": "INTEGER", "redundant_percent": "REAL", "avg_similarity": "REAL"},
        "core_algorithm": "Cosine similarity clustering for redundancy detection",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["requests", "logging", "math", "sqlite3"],
        "logic_markers": ["vector", "embedding", "cosine similarity", "collection", "centroid"],
    },
    {
        "agent_id": "PII_REDACTOR_ML_PIPELINE",
        "domain": "AI_ML",
        "purpose": "Automatically detect and redact PII from training data before model ingestion",
        "api_endpoints": [],
        "data_model": {"input_text": "TEXT", "redacted_text": "TEXT", "entities_found": "TEXT", "confidence": "REAL"},
        "core_algorithm": "Regex + Spacy-like NER pattern matching for PII (emails, SSNs, names)",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["re", "logging", "sqlite3", "json"],
        "logic_markers": ["redact", "PII", "entity", "sensitive", "filter"],
    },
    {
        "agent_id": "SYNTHETIC_DATA_GENERATOR",
        "domain": "AI_ML",
        "purpose": "Generate privacy-preserving synthetic tabular data for training",
        "api_endpoints": [],
        "data_model": {"schema": "TEXT", "row_count": "INTEGER", "fied_distribution": "TEXT", "data": "TEXT"},
        "core_algorithm": "Probabilistic distribution-based data synthesis",
        "input_type": "keyword",
        "output_format": "json_report",
        "required_imports": ["random", "logging", "sqlite3", "json", "datetime"],
        "logic_markers": ["synthetic", "seed", "distribution", "mock", "generator"],
    },
    {
        "agent_id": "PROMPT_TEMPLATE_EVOLVER",
        "domain": "AI_ML",
        "purpose": "Iteratively mutate prompt templates to maximize model performance metrics",
        "api_endpoints": [],
        "data_model": {"template_v1": "TEXT", "template_v2": "TEXT", "score_v1": "REAL", "score_v2": "REAL", "improvement": "REAL"},
        "core_algorithm": "Genetic algorithm-based prompt mutation loop",
        "input_type": "keyword",
        "output_format": "sqlite",
        "required_imports": ["logging", "sqlite3", "random", "re"],
        "logic_markers": ["evolution", "mutation", "template", "fitness", "score"],
    }
]

def main():
    for spec in AI_ML_SPECS:
        path = SPECS_DIR / f"{spec['agent_id']}.json"
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"Generated spec: {spec['agent_id']}")

if __name__ == "__main__":
    main()
