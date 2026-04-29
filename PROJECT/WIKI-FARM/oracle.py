import json
import sys
import argparse
from pathlib import Path
from collections import Counter

# NEXUS FARM-ORACLE v1.0 [RAG-LITE]
# Intelligent Knowledge Retrieval Engine for the 400+ Farmed Repositories

LIBRARY_PATH = Path(__file__).resolve().parent / "farm_library.json"

class FarmOracle:
    def __init__(self, library_path=LIBRARY_PATH):
        self.library = self._load_library(library_path)
        self.stats = self._get_stats()

    def _load_library(self, path):
        if not path.exists():
            print(f"[!] Error: Knowledge source not found at {path}")
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _get_stats(self):
        vectors = [r.get("vector", "UNKNOWN") for r in self.library]
        return Counter(vectors)

    def search(self, query, min_score=0):
        print(f"\n[ORACLE] Searching for: '{query}'")
        results = []
        keywords = query.lower().split()

        for repo in self.library:
            score = 0
            name = repo.get("name", "").lower()
            summary = repo.get("summary", "").lower()
            nexus_use = repo.get("nexus_use", "").lower()
            techs = " ".join(repo.get("techs", [])).lower()
            vector = repo.get("vector", "").lower()

            for kw in keywords:
                # Name match is highest priority
                if kw in name: score += 50
                # Vector match
                if kw in vector: score += 30
                # Summary match
                if kw in summary: score += 10
                # Use match
                if kw in nexus_use: score += 15
                # Tech match
                if kw in techs: score += 5

            if score > min_score:
                results.append({
                    "name": repo.get("name"),
                    "vector": repo.get("vector"),
                    "summary": repo.get("summary"),
                    "nexus_use": repo.get("nexus_use"),
                    "score": score,
                    "techs": repo.get("techs")
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def print_results(self, results, limit=5):
        if not results:
            print("  [!] No matches found in the NEXUS Vault.")
            return

        print(f"  [+] Found {len(results)} matches. Showing TOP {min(limit, len(results))}:\n")
        
        for i, res in enumerate(results[:limit], 1):
            print(f"  {i}. 📂 [{res['vector'].upper()}] {res['name']} (Score: {res['score']})")
            print(f"     📜 Суть: {res['summary']}")
            print(f"     💡 NEXUS USE: {res['nexus_use']}")
            print(f"     🛠 Tech: {', '.join(res['techs'][:5])}")
            print("-" * 50)

    def banner(self):
        print("\n" + "=" * 60)
        print("   NEXUS FARM-ORACLE v1.0 — Intelligence Retrieval")
        print(f"   Indexed Repositories: {len(self.library)}")
        print(f"   Strategic Vectors: {len(self.stats)}")
        print("=" * 60)

def main():
    oracle = FarmOracle()
    oracle.banner()

    parser = argparse.ArgumentParser(description="NEXUS FARM-Oracle CLI")
    parser.add_argument("query", nargs="?", help="Search query (e.g., 'osint security')")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Limit results")
    args = parser.parse_args()

    if args.query:
        res = oracle.search(args.query)
        oracle.print_results(res, limit=args.limit)
    else:
        # Interactive mode
        while True:
            try:
                q = input("\n[FARM-ORACLE] Query (or 'exit'): ").strip()
                if q.lower() in ("exit", "quit", "q"): break
                if not q: continue
                res = oracle.search(q)
                oracle.print_results(res, limit=args.limit)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
