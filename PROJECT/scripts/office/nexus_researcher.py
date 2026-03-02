import os
import sys
import trafilatura
from datetime import datetime

# Precision Research Agent
# Использует trafilatura для глубокого извлечения контента и его структурирования.

def research_topic(url):
    print(f"🔍 Researching URL: {url}")
    
    # 1. Скрапинг контента
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"❌ Failed to fetch content from {url}")
        return False
        
    # 2. Извлечение текста (LLM-ready markdown)
    content = trafilatura.extract(downloaded, include_comments=False, include_tables=True, output_format="markdown")
    
    if not content:
        print("❌ Failed to extract meaningful content.")
        return False
        
    print(f"✅ Extracted {len(content)} characters of clean text.")
    
    # 3. Сохранение результата
    output_dir = os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "outputs", "research")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.split("//")[-1].split("/")[0].replace(".", "_")
    output_path = os.path.join(output_dir, f"research_{domain}_{timestamp}.md")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Research Report: {url}\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n\n")
        f.write("---\n\n")
        f.write(content)
        
    print(f"📄 Full report saved to: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nexus_researcher.py <URL>")
        # Default for test
        research_topic("https://github.com/langchain-ai/langgraph")
    else:
        research_topic(sys.argv[1])
