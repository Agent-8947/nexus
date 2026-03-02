import os
import sys
import glob

# Adaptive RAG: Динамический поиск по документации с переключением стратегий
class AdaptiveRAG:
    def __init__(self, docs_path=None):
        self.docs_path = docs_path or os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "DOCS")

    def search(self, query):
        print(f"🔎 Adaptive Search: '{query}'")
        
        # Стратегия 1: Keyword-based поиск в локальных документах
        results = self._local_search(query)
        
        if results:
            print(f"✅ Found {len(results)} local matches.")
            return results
            
        print("⚠️ No direct local matches. Switching to Semantic Search (MOCK)...")
        # Здесь бы вызывался векторный поиск или LLM-поиск
        return ["No relevant local docs found. Consider running Researcher Agent."]

    def _local_search(self, query):
        matches = []
        files = glob.glob(os.path.join(self.docs_path, "*.md"))
        
        for f_path in files:
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        # Берем кусок текста вокруг первого совпадения
                        idx = content.lower().find(query.lower())
                        snippet = content[max(0, idx-50):min(len(content), idx+150)]
                        matches.append({
                            "file": os.path.basename(f_path),
                            "snippet": f"...{snippet}..."
                        })
            except: continue
        return matches

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Architecture"
    rag = AdaptiveRAG()
    res = rag.search(query)
    for r in res:
        print(f"\n📄 {r.get('file', 'N/A')}:\n {r.get('snippet', r)}")
