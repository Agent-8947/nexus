import json
import os

def localize_data(raw_data, lang):
    localized = {}
    
    # Mapping of category names
    cat_map = {
        "en": {
            "LLM Training and Fine-Tuning": "Training & Fine-Tuning",
            "LLM Application Development": "App Development",
            "LLM RAG": "RAG (Search & Knowledge)",
            "LLM Inference": "Inference (Running Models)",
            "LLM Serving": "Serving (Hosting)",
            "LLM Data Extraction": "Data Extraction",
            "LLM Data Generation": "Synthetic Data",
            "LLM Agents": "AI Agents",
            "LLM Evaluation": "Evaluation & Testing",
            "LLM Monitoring": "Monitoring",
            "LLM Prompts": "Prompt Engineering",
            "LLM Structured Outputs": "Structured Data",
            "LLM Safety and Security": "Safety & Security",
            "LLM Embedding Models": "Vector Embeddings",
            "Others": "Miscellaneous"
        },
        "uk": {
            "LLM Training and Fine-Tuning": "Навчання та донавчання",
            "LLM Application Development": "Розробка додатків",
            "LLM RAG": "RAG (Пошук та знання)",
            "LLM Inference": "Запуск моделей",
            "LLM Serving": "Сервінг (Хостинг)",
            "LLM Data Extraction": "Витяг даних",
            "LLM Data Generation": "Синтетичні дані",
            "LLM Agents": "AI Агенти",
            "LLM Evaluation": "Оцінка та тестування",
            "LLM Monitoring": "Моніторинг",
            "LLM Prompts": "Промпт-інжиніринг",
            "LLM Structured Outputs": "Структуровані дані",
            "LLM Safety and Security": "Безпека",
            "LLM Embedding Models": "Векторні ембедінги",
            "Others": "Інше"
        },
        "ru": {
            "LLM Training and Fine-Tuning": "Обучение и дообучение",
            "LLM Application Development": "Разработка приложений",
            "LLM RAG": "RAG (Поиск и знания)",
            "LLM Inference": "Запуск моделей",
            "LLM Serving": "Хостинг моделей",
            "LLM Data Extraction": "Извлечение данных",
            "LLM Data Generation": "Синтетические данные",
            "LLM Agents": "AI Агенты",
            "LLM Evaluation": "Оценка и тестирование",
            "LLM Monitoring": "Мониторинг",
            "LLM Prompts": "Промпт-инжиниринг",
            "LLM Structured Outputs": "Структурированные данные",
            "LLM Safety and Security": "Безопасность",
            "LLM Embedding Models": "Векторные эмбеддинги",
            "Others": "Прочее"
        }
    }

    for section, items in raw_data.items():
        if section not in cat_map[lang]:
            localized_section = section
        else:
            localized_section = cat_map[lang][section]
            
        localized_items = []
        for item in items:
            name = item['name']
            orig_desc = item['original_description']
            
            # Simple "down-to-earth" simplification rules (Heuristic)
            if lang == "uk":
                simplified = f"Інструмент для: {orig_desc}. Дозволяє зручно працювати з моделями."
                use_case = f"Корисно, коли вам потрібно {orig_desc.lower()} без зайвої складності."
                full_desc = f"{name} — це потужне рішення для {orig_desc.lower()}. Воно фокусується на швидкому результаті та зручності для розробника."
                example = f"# Почнемо роботу з {name}\n# (Приклад коду буде автоматизовано)"
            elif lang == "ru":
                simplified = f"Инструмент для: {orig_desc}. Позволяет удобно работать с моделями."
                use_case = f"Полезно, когда вам нужно {orig_desc.lower()} без лишних сложностей."
                full_desc = f"{name} — это мощное решение для {orig_desc.lower()}. Оно фокусируется на быстром результате и удобстве для разработчика."
                example = f"# Начнем работу с {name}\n# (Пример кода будет автоматизирован)"
            else:
                simplified = f"Tool for: {orig_desc}. Simplifies LLM workflows."
                use_case = f"Ideal when you need to {orig_desc.lower()} effectively."
                full_desc = f"{name} is a robust library for {orig_desc.lower()}. It provides a developer-friendly API for high-level tasks."
                example = f"# Getting started with {name}\n# (Code example placeholder)"
                
            localized_items.append({
                "name": name,
                "slug": item['slug'],
                "desc": simplified,
                "url": item['url'],
                "use_case": use_case,
                "full_desc": full_desc,
                "example": example
            })
            
        localized[localized_section] = localized_items
        
    return localized

def main():
    root_path = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\LLM-TOOLKIT-PORTAL\src\data'
    raw_path = os.path.join(root_path, 'toolkit_raw.json')
    
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    for lang in ['en', 'uk', 'ru']:
        localized = localize_data(raw_data, lang)
        output_path = os.path.join(root_path, 'locales', f'{lang}.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(localized, f, indent=2, ensure_ascii=False)
        print(f"Generated {lang}.json")

if __name__ == "__main__":
    main()
