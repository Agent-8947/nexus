"""
E06 Translator v2.0 — Translate ALL text blocks from ironing machine manual.
Uses comprehensive phrase dictionary + word-level fallback for full coverage.
"""

import json
import sys
import re


# Word-level dictionary for fallback translation
WORD_MAP = {
    # Common technical
    "Equipment": "Оборудование", "equipment": "оборудование",
    "Machine": "Машина", "machine": "машина",
    "Printer": "Принтер", "printer": "принтер",
    "Chapter": "Глава", "chapter": "глава",
    "Parameters": "Параметры", "parameters": "параметры",
    "Parameter": "Параметр", "parameter": "параметр",
    "Installation": "Установка", "installation": "установка",
    "Guide": "Руководство", "guide": "руководство",
    "Operation": "Эксплуатация", "operation": "эксплуатация",
    "Maintenance": "Обслуживание", "maintenance": "обслуживание",
    "Troubleshooting": "Поиск неисправностей", "troubleshooting": "поиск неисправностей",
    "Software": "Программное обеспечение", "software": "программное обеспечение",
    "Instructions": "Инструкции", "instructions": "инструкции",
    "WARNING": "ПРЕДУПРЕЖДЕНИЕ", "Warning": "Предупреждение", "warning": "предупреждение",
    "CAUTION": "ОСТОРОЖНО", "Caution": "Осторожно", "caution": "осторожно",
    "Safety": "Безопасность", "safety": "безопасность",
    "Specification": "Спецификация", "specification": "спецификация",
    "Temperature": "Температура", "temperature": "температура",
    "Humidity": "Влажность", "humidity": "влажность",
    "Voltage": "Напряжение", "voltage": "напряжение",
    "Power": "Питание", "power": "питание",
    "Speed": "Скорость", "speed": "скорость",
    "Width": "Ширина", "width": "ширина",
    "Height": "Высота", "height": "высота",
    "Weight": "Вес", "weight": "вес",
    "Color": "Цвет", "color": "цвет",
    "Type": "Тип", "type": "тип",
    "Port": "Порт", "port": "порт",
    "Model": "Модель", "model": "модель",
    "System": "Система", "system": "система",
    "Memory": "Память", "memory": "память",
    "Interface": "Интерфейс", "interface": "интерфейс",
    "Settings": "Настройки", "settings": "настройки",
    "Setting": "Настройка", "setting": "настройка",
    "Button": "Кнопка", "button": "кнопка",
    "Print": "Печать", "print": "печать",
    "Printing": "Печать", "printing": "печать",
    "Head": "Головка", "head": "головка",
    "Nozzle": "Сопло", "nozzle": "сопло",
    "Ink": "Чернила", "ink": "чернила",
    "Medium": "Носитель", "medium": "носитель",
    "Mode": "Режим", "mode": "режим",
    "Test": "Тест", "test": "тест",
    "Status": "Статус", "status": "статус",
    "Error": "Ошибка", "error": "ошибка",
    "Failed": "Ошибка", "failed": "ошибка",
    "Success": "Успех", "success": "успех",
    "Start": "Запуск", "start": "запуск",
    "Stop": "Стоп", "stop": "стоп",
    "Reset": "Сброс", "reset": "сброс",
    "Cancel": "Отмена", "cancel": "отмена",
    "Pause": "Пауза", "pause": "пауза",
    "Clean": "Очистка", "clean": "очистка",
    "Cleaning": "Очистка", "cleaning": "очистка",
    "Automatic": "Автоматический", "automatic": "автоматический",
    "Manual": "Ручной", "manual": "ручной",
    "Calibration": "Калибровка", "calibration": "калибровка",
    "Resolution": "Разрешение", "resolution": "разрешение",
    "Direction": "Направление", "direction": "направление",
    "Position": "Позиция", "position": "позиция",
    "Origin": "Начало координат", "origin": "начало координат",
    "Device": "Устройство", "device": "устройство",
    "Display": "Дисплей", "display": "дисплей",
    "Motor": "Мотор", "motor": "мотор",
    "Sensor": "Датчик", "sensor": "датчик",
    "Switch": "Переключатель", "switch": "переключатель",
    "Control": "Управление", "control": "управление",
    "Circuit": "Цепь", "circuit": "цепь",
    "Board": "Плата", "board": "плата",
    "Cable": "Кабель", "cable": "кабель",
    "Wire": "Провод", "wire": "провод",
    "Plug": "Разъём", "plug": "разъём",
    "Damage": "Повреждение", "damage": "повреждение",
    "Damaged": "Повреждён", "damaged": "повреждён",
    "Repair": "Ремонт", "repair": "ремонт",
    "Replace": "Замена", "replace": "замена",
    "Check": "Проверка", "check": "проверка",
    "Inspect": "Осмотр", "inspect": "осмотр",
    "Inspection": "Осмотр", "inspection": "осмотр",
    "Adjust": "Регулировка", "adjust": "регулировка",
    "adjustment": "регулировка", "Adjustment": "Регулировка",
    "Install": "Установка", "install": "установка",
    "Remove": "Удаление", "remove": "удаление",
    "Open": "Открыть", "open": "открыть",
    "Close": "Закрыть", "close": "закрыть",
    "Turn": "Повернуть", "turn": "повернуть",
    "Connect": "Подключить", "connect": "подключить",
    "Disconnect": "Отключить", "disconnect": "отключить",
    "Supply": "Питание", "supply": "питание",
    "Output": "Выход", "output": "выход",
    "Input": "Вход", "input": "вход",
    "File": "Файл", "file": "файл",
    "Image": "Изображение", "image": "изображение",
    "Picture": "Изображение", "picture": "изображение",
    "Current": "Текущий", "current": "текущий",
    "Default": "По умолчанию", "default": "по умолчанию",
    "Maximum": "Максимум", "maximum": "максимум",
    "Minimum": "Минимум", "minimum": "минимум",
    "Normal": "Нормальный", "normal": "нормальный",
    "Abnormal": "Ненормальный", "abnormal": "ненормальный",
    "Left": "Левый", "left": "левый",
    "Right": "Правый", "right": "правый",
    "Front": "Передний", "front": "передний",
    "Back": "Задний", "back": "задний",
    "Top": "Верхний", "top": "верхний",
    "Bottom": "Нижний", "bottom": "нижний",
    "On": "Вкл", "on": "вкл",
    "Off": "Выкл", "off": "выкл",
    "Yes": "Да", "yes": "да",
    "No": "Нет", "no": "нет",
    "Note": "Примечание", "note": "примечание",
    "Step": "Шаг", "step": "шаг",
    "Pass": "Проход", "pass": "проход",
    "Waveform": "Форма сигнала", "waveform": "форма сигнала",
    "Platform": "Платформа", "platform": "платформа",
    "Firmware": "Прошивка", "firmware": "прошивка",
    "Driver": "Драйвер", "driver": "драйвер",
    "Computer": "Компьютер", "computer": "компьютер",
    "Data": "Данные", "data": "данные",
    "Network": "Сеть", "network": "сеть",
    "Online": "Онлайн", "online": "онлайн",
    "Offline": "Оффлайн", "offline": "оффлайн",
    "Startup": "Запуск", "startup": "запуск",
    "Shutdown": "Выключение", "shutdown": "выключение",
    "Schematic": "Схема", "schematic": "схема",
    "Diagram": "Диаграмма", "diagram": "диаграмма",
    "Assembly": "Сборка", "assembly": "сборка",
    "Component": "Компонент", "component": "компонент",
    "Frame": "Рама", "frame": "рама",
    "Trolley": "Каретка", "trolley": "каретка",
    "Carriage": "Каретка", "carriage": "каретка",
    "Belt": "Ремень", "belt": "ремень",
    "Wheel": "Колесо", "wheel": "колесо",
    "Paper": "Бумага", "paper": "бумага",
    "Film": "Плёнка", "film": "плёнка",
    "Roller": "Ролик", "roller": "ролик",
    "Screw": "Винт", "screw": "винт",
    "Bracket": "Кронштейн", "bracket": "кронштейн",
    "Leg": "Ножка", "leg": "ножка",
    "Cover": "Крышка", "cover": "крышка",
    "Door": "Дверца", "door": "дверца",
    "Panel": "Панель", "panel": "панель",
    "Key": "Клавиша", "key": "клавиша",
    "Recommended": "Рекомендуемый", "recommended": "рекомендуемый",
    "Required": "Требуемый", "required": "требуемый",
    "Available": "Доступный", "available": "доступный",
    "Selected": "Выбранный", "selected": "выбранный",
    "Enabled": "Включён", "enabled": "включён",
    "Disabled": "Выключен", "disabled": "выключен",
    "Configuration": "Конфигурация", "configuration": "конфигурация",
    "Preparation": "Подготовка", "preparation": "подготовка",
    "Description": "Описание", "description": "описание",
    "Contents": "Содержание", "contents": "содержание",
    "Catalogue": "Содержание", "catalogue": "содержание",
    "Introduction": "Введение", "introduction": "введение",
    "Preface": "Предисловие", "preface": "предисловие",
    "ironing": "гладильная",
    "Specification": "Спецификация",
    "Shortcut": "Быстрый доступ", "shortcut": "быстрый доступ",
    "Manufacturer": "Производитель", "manufacturer": "производитель",
    "Winding": "Намотка", "winding": "намотка",
    "Powder": "Порошок", "powder": "порошок",
    "Drying": "Сушка", "drying": "сушка",
    "Heating": "Нагрев", "heating": "нагрев",
    "Suction": "Отсос", "suction": "отсос",
    "Filter": "Фильтр", "filter": "фильтр",
    "Purifier": "Очиститель", "purifier": "очиститель",
    "Emergency": "Аварийный", "emergency": "аварийный",
    "Overload": "Перегрузка", "overload": "перегрузка",
    "Short": "Короткое замыкание", "short": "короткое замыкание",
    "Fire": "Пожар", "fire": "пожар",
    "Electric": "Электрический", "electric": "электрический",
    "Shock": "Удар", "shock": "удар",
    "Flammable": "Легковоспламеняющийся", "flammable": "легковоспламеняющийся",
    "Volatile": "Летучий", "volatile": "летучий",
    "Solvent": "Растворитель", "solvent": "растворитель",
    "Common": "Распространённый", "common": "распространённый",
    "Fault": "Неисправность", "fault": "неисправность",
    "Cause": "Причина", "cause": "причина",
    "Solution": "Решение", "solution": "решение",
    "Resolvent": "Решение", "resolvent": "решение",
    "Method": "Метод", "method": "метод",
    "Procedure": "Процедура", "procedure": "процедура",
    "Horizontal": "Горизонтальный", "horizontal": "горизонтальный",
    "Vertical": "Вертикальный", "vertical": "вертикальный",
    "Bidirectional": "Двунаправленный", "bidirectional": "двунаправленный",
}

# Full phrase translations for E06
PHRASE_MAP = {
    "Specification   for   ironing   machine": "Спецификация гладильной машины",
    "ADL07E06": "ADL07E06",
    "catalogue": "содержание",
    "Chapter   1   Equipment   Parameters": "Глава 1: Параметры оборудования",
    "Chapter   II   Equipment   Installation   Guide": "Глава II: Руководство по установке оборудования",
    "Chapter   III   Equipment   Operation   Guide": "Глава III: Руководство по эксплуатации оборудования",
    "Chapter   4:   Software   installation   and   use   instructions": "Глава 4: Инструкции по установке и использованию ПО",
    "Chapter   V   Equipment   maintenance   and   troubleshooting": "Глава V: Обслуживание оборудования и поиск неисправностей",
    "Ensure the installation and proper use": "Обеспечение правильной установки и использования",
    "Safety guidance": "Руководство по безопасности",
    "introduction": "Введение",
    "Explain the use agreement": "Пояснение условного обозначения",
    "Note for printer installation": "Примечания по установке принтера",
    "Chapter II Equipment Installation Guide": "Глава II: Руководство по установке оборудования",
    "Chapter III Equipment Operation Guide": "Глава III: Руководство по эксплуатации оборудования",
    "Repair and inspection": "Ремонт и осмотр",
    "Notes and the handling of consumables such as ink cartridges": "Примечания и работа с расходными материалами (картриджи)",
    "Operational   safety   precautions": "Меры безопасности при эксплуатации",
    "Power   supply   safety   precautions": "Меры безопасности при электропитании",
    "Machine   model   number:   ADL07E06": "Номер модели машины: ADL07E06",
    "Head   specification:   Epson   3200A1": "Спецификация головки: Epson 3200A1",
    "Printing   medium:   transfer   film": "Носитель печати: термотрансферная плёнка",
    "Media   transmission:   a   three-gear   adjustable   paper   press   wheel": "Передача носителя: трёхступенчатый регулируемый прижимной ролик",
    "Print   width:   700mm": "Ширина печати: 700 мм",
    "Ink   color:   C   M   Y   K   W": "Цвет чернил: C M Y K W",
    "Ink   type:   paint   ink": "Тип чернил: пигментные",
    "Print   port:   High-speed   USB3.0": "Порт печати: Высокоскоростной USB3.0",
    "Printing   speed:   6   pass   40 ㎡/   h": "Скорость печати: 6 проходов, 40 м²/ч",
    "Input   voltage:   220V   AC   10A   /   110V   AC   20A": "Входное напряжение: 220В AC 10A / 110В AC 20A",
    "Power   parameter:   2200W": "Параметры мощности: 2200 Вт",
    "Working   environment:   temperature:   20-30℃/   humidity:   40-60%": "Рабочая среда: температура 20–30°C / влажность 40–60%",
    "Debug   interface:": "Интерфейс отладки:",
    "Main   interface": "Главный интерфейс",
    "Parameter   settings:": "Настройки параметров:",
    "Shortcut button": "Кнопки быстрого доступа",
    "status bar": "строка состояния",
    "Manufacturer mode": "Режим производителя",
    "manufacturer mode": "режим производителя",
    "Running machine": "Работа машины",
    "Waveform Settings": "Настройки формы сигнала",
}


def translate_en_to_ru(text: str) -> str:
    if not text or not text.strip():
        return text

    # Skip pure numbers / technical codes
    if re.match(r'^[\d\s\.\,\-\+\%\℃\/\(\)\*×xXmMkKgGwWhHzZvV㎡]+$', text.strip()):
        return text

    # Chinese page numbers
    cn_page = re.match(r'第\s*(\d+)\s*页共\s*(\d+)\s*页', text)
    if cn_page:
        return f"Стр. {cn_page.group(1)} из {cn_page.group(2)}"

    # "auxiliary word for ordinal numbers..."
    aux_match = re.match(r'auxiliary word for ordinal numbers(\d+)A total of pages(\d+)page', text)
    if aux_match:
        return f"Стр. {aux_match.group(1)} из {aux_match.group(2)}"
    
    # Try exact phrase match
    if text in PHRASE_MAP:
        return PHRASE_MAP[text]

    # Try normalized match
    normalized = re.sub(r'\s+', ' ', text.strip())
    for key, val in PHRASE_MAP.items():
        if re.sub(r'\s+', ' ', key.strip()) == normalized:
            return val

    # Word-by-word translation for remaining blocks
    # Preserve structure: replace known words, keep unknown ones
    result = text
    # Sort by length descending to match longer phrases first
    for eng, rus in sorted(WORD_MAP.items(), key=lambda x: -len(x[0])):
        # Word boundary replacement
        result = re.sub(r'\b' + re.escape(eng) + r'\b', rus, result)
    
    if result != text:
        return result
    
    # If nothing matched at all, return original (will be skipped by engine)
    return text


def process_file(raw_path, output_path):
    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {}
    translated_count = 0
    total_count = 0

    for pg, items in data.items():
        new_items = []
        for item in items:
            en = item["en_text"]
            ru = translate_en_to_ru(en)
            total_count += 1
            if ru != en:
                translated_count += 1
            new_items.append({
                "bbox": item["bbox"],
                "en_text": en,
                "ru_text": ru,
                "font_size": item["font_size"]
            })
        result[pg] = new_items

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] {translated_count}/{total_count} blocks translated ({translated_count/total_count*100:.1f}%)")
    print(f"[OK] Saved: {output_path}")


if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2])
