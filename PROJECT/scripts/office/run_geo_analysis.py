import os
import sys
import json
from pyseoanalyzer import analyze
from datetime import datetime

def run_geo_analysis(url="http://localhost:4321"):
    print(f"🧠 Starting GEO & AI Analysis for: {url}")
    
    output_dir = os.path.join("e:\\Downloads\\--ANTIGRAVITY store\\IDE-optimus\\PROJECT", "outputs", "geo_analysis")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"geo_report_{timestamp}.json")
    
    # Мы активируем LLM-анализ, если ключ API доступен
    # Для этого pyseoanalyzer использует переменную окружения ANTHROPIC_API_KEY
    run_llm = "ANTHROPIC_API_KEY" in os.environ
    if run_llm:
        print("✨ Anthropic API Key found. Enabling AI content evaluation.")
    else:
        print("⚠️ Anthropic API Key NOT found. running technical-only analysis.")

    try:
        # analyze(site, sitemap=None, analyze_headings=True, analyze_extra_tags=True)
        # Примечание: pyseoanalyzer может требовать sitemap или будет краулить от главной
        results = analyze(url, analyze_headings=True, analyze_extra_tags=True)
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"\n✅ GEO Analysis complete! Report saved to: {report_file}")
        
        # Краткий отчет в консоль
        pages_count = len(results.get("pages", []))
        print(f"📊 Analyzed {pages_count} pages.")
        
        return True
    except Exception as e:
        print(f"❌ Error during GEO analysis: {e}")
        return False

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4321"
    run_geo_analysis(target_url)
