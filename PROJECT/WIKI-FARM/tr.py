import json
import re
from deep_translator import GoogleTranslator
import concurrent.futures

def main():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            text = f.read()

        m = re.search(r'(const REPO_DATA\s*=\s*)(\[.*?\])(;)', text, re.DOTALL)
        if not m:
            print("Failed to find REPO_DATA")
            return

        prefix = m.group(1)
        data = json.loads(m.group(2))
        suffix = m.group(3)

        translator_en = GoogleTranslator(source='ru', target='en')
        translator_ua = GoogleTranslator(source='ru', target='uk')

        def process_item(item):
            try:
                if 'summary_en' not in item:
                    item['summary_en'] = translator_en.translate(item.get('summary', ''))
                if 'summary_ua' not in item:
                    item['summary_ua'] = translator_ua.translate(item.get('summary', ''))
                if 'nexus_use_en' not in item:
                    item['nexus_use_en'] = translator_en.translate(item.get('nexus_use', ''))
                if 'nexus_use_ua' not in item:
                    item['nexus_use_ua'] = translator_ua.translate(item.get('nexus_use', ''))
            except Exception as e:
                item['summary_en'] = item.get('summary', '')
                item['summary_ua'] = item.get('summary', '')
                item['nexus_use_en'] = item.get('nexus_use', '')
                item['nexus_use_ua'] = item.get('nexus_use', '')
            return item

        print(f"Translating {len(data)} items...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(process_item, data))

        new_data_str = json.dumps(results, ensure_ascii=False)
        new_text = text[:m.start()] + prefix + new_data_str + suffix + text[m.end():]

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_text)

        print("Successfully translated data.")
    except Exception as e:
        print(f"Error: {str(e)}")

main()
