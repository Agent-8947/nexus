import json

# Comprehensive Manual Translation for ADL07E06 & general manual terms
def translate_technical_term(text):
    mapping = {
        "Specification for ironing machine": "Спецификация гладильной машины",
        "ADL07E06": "ADL07E06",
        "Henan Yindu Digital Technology Co., LTD": "Henan Yindu Digital Technology Co., LTD",
        "HENAN AUDLEY DIGITAL CO.,LTD": "HENAN AUDLEY DIGITAL CO.,LTD",
        "catalogue": "содержание",
        "Chapter 1 Equipment Parameters": "Глава 1: Параметры оборудования",
        "Chapter II Equipment Installation Guide": "Глава II: Руководство по установке оборудования",
        "Chapter III Equipment Operation Guide": "Глава III: Руководство по эксплуатации оборудования",
        "Chapter 4: Software installation and use instructions": "Глава 4: Инструкции по установке и использованию ПО",
        "Chapter V Equipment maintenance and troubleshooting": "Глава V: Обслуживание оборудования и поиск неисправностей",
        "Ensure the installation and proper use": "Обеспечение правильной установки и использования",
        "Safety guidance": "Руководство по безопасности",
        "introduction": "введение",
        "Explain the use agreement": "Пояснение соглашения об использовании",
        "Safety Instruction": "Инструкция по безопасности",
        "Preface": "Предисловие",
        "WARNING": "ПРЕДУПРЕЖДЕНИЕ",
        "CAUTION": "ОСТОРОЖНО",
        "Printer Installation Notes": "Примечания по установке принтера",
        "Observe the environment": "Соблюдение условий среды",
        "Power supply safety precautions": "Меры безопасности при электропитании",
        "Operational safety precautions": "Меры безопасности при эксплуатации",
        "Repair and inspection": "Ремонт и осмотр",
        "Maintenance and inspection": "Техническое обслуживание и осмотр",
        "Notes and the handling of consumables such as ink cartridges": "Примечания и работа с расходными материалами, такими как картриджи",
        "Machine model number": "Номер модели машины",
        "Head specification": "Спецификация головки",
        "Printing medium": "Носитель для печати",
        "Media transmission": "Передача носителя",
        "Print width": "Ширина печати",
        "Ink color": "Цвет чернил",
        "Ink type": "Тип чернил",
        "Print port": "Порт печати",
        "Printing speed": "Скорость печати",
        "Input voltage": "Входное напряжение",
        "Power parameter": "Параметры мощности",
        "Working environment": "Рабочая среда",
        "Ink supply method": "Метод подачи чернил",
        "Installation Guide": "Руководство по установке",
        "Operation Guide": "Руководство по эксплуатации",
        "Software startup and online": "Запуск ПО и онлайн-режим",
        "Main interface": "Главный интерфейс",
        "Shortcut button": "Кнопки быстрого доступа",
        "status bar": "строка состояния",
        "Manufacturer mode": "Режим производителя",
        "Running machine": "Работа машины",
        "Waveform Settings": "Настройки формы сигнала",
        "Troubleshooting": "Поиск и устранение неисправностей",
        "resolvent": "решение",
        "Common fault": "Типичная неисправность",
        "Failed to open file": "Ошибка открытия файла",
        "System initialization action execution failed": "Ошибка выполнения инициализации системы",
        "Device disconnected": "Устройство отключено",
        "Print failed": "Ошибка печати",
    }
    
    # Check for exact matches
    if text in mapping:
        return mapping[text]
    
    # Check for "auxiliary word for ordinal numbers..." page headers
    if "auxiliary word for ordinal numbers" in text:
        try:
            parts = text.split("A total of pages")
            page_num = "".join(filter(str.isdigit, parts[0]))
            total_pages = "".join(filter(str.isdigit, parts[1]))
            return f"Стр. {page_num} из {total_pages}"
        except:
            return text
            
    # Simple replace for commonly occurring words to capture mixed text
    res = text
    subs = {
        "Chapter": "Глава",
        "Equipment": "Оборудование",
        "Parameters": "Параметры",
        "Maintenance": "Обслуживание",
        "Operation": "Эксплуатация",
        "Installation": "Установка",
        "Temperature": "Температура",
        "Humidity": "Влажность",
        "Voltage": "Напряжение"
    }
    for k, v in subs.items():
        if k in res and len(res) < 50: # Only for short titles/labels
            res = res.replace(k, v)
            
    return res

def bulk_translate(raw_json_path, output_json_path):
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    translated_data = {}
    for pg, items in data.items():
        new_items = []
        for item in items:
            ru_text = translate_technical_term(item['en_text'])
            new_items.append({
                "bbox": item['bbox'],
                "en_text": item['en_text'],
                "ru_text": ru_text,
                "font_size": item['font_size']
            })
        translated_data[pg] = new_items
        
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    bulk_translate(sys.argv[1], sys.argv[2])
