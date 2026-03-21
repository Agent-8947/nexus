import json
import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    return re.sub(r'-+', '-', text).strip('-')

def update_localized_with_slugs():
    root_path = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\LLM-TOOLKIT-PORTAL\src\data\locales'
    
    for lang in ['en', 'uk', 'ru']:
        file_path = os.path.join(root_path, f'{lang}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        new_data = {}
        for section, items in data.items():
            new_items = []
            for item in items:
                item['slug'] = slugify(item['name'])
                # Placeholder for detailed content if not present
                if 'full_desc' not in item:
                    if lang == "uk":
                        item['full_desc'] = f"Детальний опис для {item['name']} з прикладами коду та сценаріями використання."
                        item['example'] = f"# Приклад використання {item['name']}\nprint('Приклад завантажується...')"
                        item['use_case'] = "Сценарій використання: автоматизація робочих процесів з LLM."
                    elif lang == "ru":
                        item['full_desc'] = f"Подробное описание для {item['name']} с примерами кода и сценариями использования."
                        item['example'] = f"# Пример использования {item['name']}\nprint('Пример загружается...')"
                        item['use_case'] = "Сценарий использования: автоматизация рабочих процессов с LLM."
                    else:
                        item['full_desc'] = f"Detailed description for {item['name']} with code examples and use cases."
                        item['example'] = f"# Usage example for {item['name']}\nprint('Example loading...')"
                        item['use_case'] = "Standard use case: streamlining LLM development workflows."
                
                new_items.append(item)
            new_data[section] = new_items
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        print(f"Updated {lang}.json with slugs and placeholders.")

if __name__ == "__main__":
    update_localized_with_slugs()
