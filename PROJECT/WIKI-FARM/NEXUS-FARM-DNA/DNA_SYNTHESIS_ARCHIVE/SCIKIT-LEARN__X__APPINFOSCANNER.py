#!/usr/bin/env python3
"""
AGENT ID: SCIKIT-LEARN__X__APPINFOSCANNER [GEN-1 ANALYZER]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Role: ML Pattern Recognizer (Clustering)
Input: farm_library.json
Logic: K-Means clustering of repository descriptions.
"""

import json
import logging
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ── CONFIG BLOCK ────────────────────────────────────────────────────────
NODE_ID = "SCIKIT-LEARN__X__APPINFOSCANNER"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "farm_library.json"
N_CLUSTERS = 5
LOG_FORMAT = f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(NODE_ID)

class ML_ClusterAnalyzer:
    """Unsupervised learning engine for project classification."""
    
    def __init__(self, n_clusters: int):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')

    def analyze_clusters(self, source_path: Path):
        logger.info(f"Loading data for ML Clustering...")
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        records = []
        for url, meta in data.get("REPOSITORIES", {}).items():
            text = f"{meta.get('name')} {meta.get('description') or ''} {' '.join(meta.get('topics', []))}"
            records.append({"name": meta['name'], "text": text})

        df = pd.DataFrame(records)
        logger.info(f"Vectorizing {len(df)} documents...")
        
        # Core ML Logic
        matrix = self.vectorizer.fit_transform(df['text'])
        df['cluster'] = self.model.fit_predict(matrix)
        
        # Extracting cluster keywords
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        
        results = {"clusters": []}
        for i in range(self.n_clusters):
            cluster_terms = [terms[ind] for ind in order_centroids[i, :5]]
            cluster_apps = df[df['cluster'] == i]['name'].head(5).tolist()
            
            results["clusters"].append({
                "cluster_index": i,
                "keywords": cluster_terms,
                "representative_apps": cluster_apps
            })
            
        return results

def main():
    if not SOURCE_FILE.exists():
        logger.error("OSINT Data source missing.")
        return

    analyzer = ML_ClusterAnalyzer(n_clusters=N_CLUSTERS)
    report = analyzer.analyze_clusters(SOURCE_FILE)
    
    output_path = Path(__file__).resolve().parent / "ml_cluster_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    logger.info(f"ML Clustering complete. Repositories grouped into {N_CLUSTERS} functional families.")

if __name__ == "__main__":
    main()
