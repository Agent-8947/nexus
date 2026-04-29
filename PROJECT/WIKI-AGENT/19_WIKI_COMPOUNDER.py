#!/usr/bin/env python3
"""
NEXUS AGENT 19 - WIKI COMPOUNDER [LOOP CLOSER]
-------------------------------------------
Mission: Implement the Karpathy Compounding Loop. Take output from any agent,
extract semantic knowledge, check for duplicates, and patch or create WIKI-files.
"""

import os
import json
import time
import subprocess
from datetime import datetime

SYSTEM_PROMPT = """
AGENT 19 - WIKI COMPOUNDER. GOVERNED BY NEXUS CONSTITUTION.
You synthesize agent output into WIKI articles.

INSTRUCTIONS:
1. Extract facts, technologies, and metadata from INPUT_TEXT.
2. Perform blue-green drafting: create a detailed markdown article.
3. Content Requirement: MINIMUM 500 WORDS of deep technical analysis.
4. Output must be strictly JSON (no markdown fences).

JSON SCHEMA:
{
  "agent": "19_WIKI_COMPOUNDER",
  "action": "CREATE | PATCH | SKIP",
  "domain": "SECURITY | ROBOTICS | CODE | LEGAL | GENERAL",
  "confidence": "HIGH | MEDIUM | LOW",
  "links": [{"from": "A", "rel": "REL", "to": "B"}],
  "content": "--- [REQUIRED: 500+ WORDS OF DETAILED ANALYTICS] ---",
  "summary": "Short recap"
}
"""


class NexusCompounder:
    def __init__(self):
        self.wiki_base_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI"
        self.log_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-MAP\COMPOUND_LOG.json"
        
        # Initializing dirs
        if not os.path.exists(self.wiki_base_path):
            os.makedirs(self.wiki_base_path)

    def _call_llm(self, source_agent, output_text):
        """
        Interacts with the LLM via local OLLAMA API.
        [LAW-13: PLUGGABLE BACKENDS] -> Switched to LOCAL OLLAMA (Gemma-2)
        """
        user_prompt = f"SOURCE_AGENT: {source_agent}\nOUTPUT_TEXT:\n{output_text}"
        
        try:
            import requests
            # Targeting OLLAMA local endpoint
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "gemma4:e2b", # [NEXUS v6: GEMMA 4 UPGRADE]
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT + "\nRemember: Always use the thinking mode `<|think|>` if available for complex reasoning."},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 1.0, # Recommended for Gemma 4
                        "top_p": 0.95,
                        "num_predict": 4096
                    }
                },
                timeout=300
            )
            res_json = response.json()
            raw_result = res_json.get("message", {}).get("content", "{}")
        except Exception as e:
            print(f"[!] Local OLLAMA call failed: {e}. Mocking LLM Output...")
            # For pure offline testing purposes
            raw_result = json.dumps({
                "domain": "SECURITY",
                "search_query": "auto-test mock data CVE-2024",
                "action": "CREATE",
                "article_path": "ros2_cve_mock.md",
                "content": "---\ntitle: ROS2 CVE Mock\ndomain: SECURITY\nconfidence: HIGH\n---\n## Суть\nMock test for Compounder.\n",
                "confidence": "HIGH",
                "source_agent": source_agent
            })

        # Remove potential markdown fences protecting the JSON block
        if raw_result.startswith("```json"):
            raw_result = raw_result.split("```json")[-1].split("```")[0].strip()
        elif raw_result.startswith("```"):
            raw_result = raw_result.split("```")[-1].split("```")[0].strip()
            
        try:
            return json.loads(raw_result)
        except json.JSONDecodeError as e:
            print(f"[!] LLM Returned invalid JSON: {e}")
            return None

    def search_wiki(self, query):
        """
        Step 3 implementation: Search before committing.
        Uses local ripgrep if available, else simple python scan.
        """
        try:
            # Using ripgrep for hyper-efficient search across 1400+ files
            result = subprocess.run(
                ['rg', '-l', '-i', str(query), self.wiki_base_path], 
                capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )
            if result.stdout:
                files = [f for f in result.stdout.split('\n') if f]
                return files[0] if files else None # Return top match targeting path
        except (FileNotFoundError, Exception) as e:
            # Fallback slow search or handle rg errors
            print(f"    [!] Search error: {e}")
            # Fallback slow search
            for root, _, files in os.walk(self.wiki_base_path):
                for f in files:
                    if f.endswith('.md'):
                        if query.lower() in f.lower():
                            return os.path.join(root, f)
        return None

    def apply_knowledge(self, data: dict):
        """
        Step 4 Exec: Merging or Creating knowledge physically on disk.
        """
        action = data.get("action", "SKIP")
        
        if action == "SKIP":
            print(f"[*] SKIPPED: {data.get('skip_reason', 'Low confidence or no actionable info')}")
            return
            
        domain = data.get("domain", "GENERAL")
        domain_dir = os.path.join(self.wiki_base_path, domain)
        if not os.path.exists(domain_dir):
            os.makedirs(domain_dir)

        # Handle Create
        if action == "CREATE":
            filename = data.get("article_path", "").split("/")[-1]
            if not filename: filename = f"entity_{int(time.time())}.md"
            if not filename.endswith('.md'): filename += ".md"
            
            filepath = os.path.join(domain_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data.get("content", ""))
            print(f"[+] KNOWLEDGE CREATED: {filepath}")

        # Handle Patch
        elif action == "PATCH":
            target_file = data.get("article_path", "")
            if not target_file:
                print("[-] PATCH FAILED: No target_file provided by agent.")
                return
                
            # Naive resolution: find file in WIKI
            filepath = os.path.join(self.wiki_base_path, target_file.split("WIKI/")[-1])
            if not os.path.exists(filepath):
                print(f"[-] PATCH FAILED: File {filepath} does not exist. Halting patch.")
                return
                
            with open(filepath, "a", encoding="utf-8") as f:
                f.write("\n\n### [COMPOUND PATCH] " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                content = data.get("content", "")
                if isinstance(content, str):
                    f.write(content)
                elif isinstance(content, dict):
                    f.write("**New Facts:**\n")
                    for fact in content.get("new_facts", []):
                        f.write(f"- {fact}\n")
                    f.write("\n**Updated Links:**\n")
                    for link in content.get("updated_links", []):
                        f.write(f"- {link}\n")
            print(f"[+] KNOWLEDGE MERGED: Appended patch to {filepath}")

        # Log link extraction (Preparation for GraphRAG later)
        if data.get("links"):
            self._log_graph_relations(data.get("links"), domain)

    def _log_graph_relations(self, links, domain):
        """ Stores semantic relations for future Graph DB (Схема 3) """
        edges = []
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8") as f:
                edges = json.load(f)
                
        edges.append({
            "timestamp": time.ctime(),
            "domain": domain,
            "relations": links
        })
        
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(edges, f, indent=4)

    def run(self, source_agent, output_text):
        """ Main executor loop """
        print(f"[*] AGENT 19 [COMPOUNDER]: Processing output from {source_agent}...")
        
        payload = self._call_llm(source_agent, output_text)
        if payload:
            print(f"[*] SYNTHESIZED ACTION: {payload.get('action')} -> {payload.get('article_path', 'N/A')}")
            
            # If CREATE, ensure it doesn't already exist via local ripgrep search
            if payload.get("action") == "CREATE":
                match = self.search_wiki(payload.get("search_query", ""))
                if match:
                    print(f"[!] DUPLICATE DETECTED locally at {match}. Changing CREATE to PATCH.")
                    payload["action"] = "PATCH"
                    payload["article_path"] = match
            
            self.apply_knowledge(payload)
        else:
            print("[-] AGENT 19 ERROR: Payload extraction failed.")

if __name__ == "__main__":
    # Test stub
    test_agent = "06_WIKI_ENGINEER"
    test_output = """Мы успешно развернули ROS2 контейнер. Замечена уязвимость CVE-2024-1111 в навигационном стеке."""
    
    compounder = NexusCompounder()
    compounder.run(test_agent, test_output)
