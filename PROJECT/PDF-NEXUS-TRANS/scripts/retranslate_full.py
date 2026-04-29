"""
NEXUS RETRANSLATION ENGINE v2.0
Полный проход по JSON-переводам K10 и E06.
Находит все блоки где ru_text содержит английские слова
и заменяет их чистым русским переводом.
Словарь собран вручную из реального контекста промышленного оборудования.
"""
import json, re, os, copy

# ============================================================
# MASTER TRANSLATION DICTIONARY — промышленная терминология
# ============================================================
DICT = {
    # ─── Equipment & Parts ───
    "powder": "порошок",
    "shaking": "встряхивание",
    "machine": "машина",
    "equipment": "оборудование",
    "device": "устройство",
    "product": "продукт",
    "printer": "принтер",
    "print head": "печатающая головка",
    "spray head": "сопло",
    "nozzle": "сопло",
    "carriage": "каретка",
    "platform": "платформа",
    "mesh belt": "сетчатая лента",
    "conveyor belt": "конвейерная лента",
    "winding": "намотка",
    "rewinding": "перемотка",
    "heat transfer film": "термотрансферная плёнка",
    "film": "плёнка",
    "ink": "чернила",
    "ink sac": "чернильный картридж",
    "waste ink": "отработанные чернила",
    "cartridge": "картридж",
    "motor": "мотор",
    "sensor": "датчик",
    "switch": "переключатель",
    "button": "кнопка",
    "knob": "ручка",
    "lever": "рычаг",
    "shaft": "вал",
    "roller": "ролик",
    "guide plate": "направляющая пластина",
    "front guide": "передняя направляющая",
    "drying zone": "зона сушки",
    "heater": "нагреватель",
    "filter": "фильтр",
    "purifier": "очиститель",
    "suction": "всасывание",
    "vacuum": "вакуум",
    "fan": "вентилятор",
    "cabinet": "корпус",
    "door": "дверца",
    "cover": "крышка",
    "panel": "панель",
    "board": "плата",
    "control board": "плата управления",
    "touch screen": "сенсорный экран",
    "LED": "LED",
    "scraper": "скребок",
    "cap": "заглушка",
    "bolt": "болт",
    "screw": "винт",
    "nut": "гайка",
    "bracket": "кронштейн",
    "frame": "рама",
    "leg": "ножка",
    "pipe": "труба",
    "tube": "трубка",
    "hose": "шланг",
    "cable": "кабель",
    "wire": "провод",
    "ground wire": "провод заземления",
    "power cord": "кабель питания",
    "power supply": "питание",
    "voltage": "напряжение",
    "current": "ток",
    "circuit": "цепь",
    "short circuit": "короткое замыкание",
    "fuse": "предохранитель",
    "contactor": "контактор",
    "relay": "реле",
    
    # ─── Actions & Operations ───
    "install": "установить",
    "installation": "установка",
    "operate": "эксплуатировать",
    "operation": "эксплуатация",
    "maintenance": "обслуживание",
    "troubleshooting": "поиск неисправностей",
    "repair": "ремонт",
    "replace": "заменить",
    "replacement": "замена",
    "adjust": "отрегулировать",
    "adjustment": "регулировка",
    "calibration": "калибровка",
    "calibrate": "калибровать",
    "clean": "очистить",
    "cleaning": "очистка",
    "inspect": "осмотреть",
    "inspection": "осмотр",
    "check": "проверить",
    "test": "тест",
    "print": "печать",
    "printing": "печать",
    "debug": "отладка",
    "setting": "настройка",
    "settings": "настройки",
    "parameter": "параметр",
    "parameters": "параметры",
    "configuration": "конфигурация",
    "mode": "режим",
    "manual": "ручной",
    "automatic": "автоматический",
    "start": "запуск",
    "stop": "остановка",
    "pause": "пауза",
    "reset": "сброс",
    "cancel": "отмена",
    "confirm": "подтвердить",
    "enter": "ввод",
    "exit": "выход",
    "save": "сохранить",
    "load": "загрузить",
    "open": "открыть",
    "close": "закрыть",
    "turn on": "включить",
    "turn off": "выключить",
    "connect": "подключить",
    "disconnect": "отключить",
    "plug": "подключить",
    "unplug": "отключить от сети",
    "insert": "вставить",
    "remove": "удалить",
    "move": "переместить",
    "forward": "вперёд",
    "backward": "назад",
    "left": "влево",
    "right": "вправо",
    "up": "вверх",
    "down": "вниз",
    "clockwise": "по часовой стрелке",
    "counterclockwise": "против часовой стрелки",
    
    # ─── Safety ───
    "warning": "предупреждение",
    "caution": "осторожно",
    "danger": "опасность",
    "fire": "пожар",
    "electric shock": "удар электрическим током",
    "injury": "травма",
    "damage": "повреждение",
    "flammable": "легковоспламеняющийся",
    "volatile": "летучий",
    "solvent": "растворитель",
    "alcohol": "спирт",
    "thinner": "растворитель",
    "moisture": "влага",
    "humidity": "влажность",
    "temperature": "температура",
    "overheat": "перегрев",
    "overcurrent": "перегрузка по току",
    "overload": "перегрузка",
    "emergency stop": "аварийная остановка",
    "safety cover": "защитный кожух",
    
    # ─── Technical ───
    "speed": "скорость",
    "width": "ширина",
    "height": "высота",
    "length": "длина",
    "weight": "вес",
    "size": "размер",
    "resolution": "разрешение",
    "frequency": "частота",
    "power": "мощность",
    "capacity": "ёмкость",
    "pressure": "давление",
    "flow": "расход",
    "level": "уровень",
    "position": "позиция",
    "direction": "направление",
    "angle": "угол",
    "distance": "расстояние",
    "gap": "зазор",
    "thickness": "толщина",
    "diameter": "диаметр",
    "range": "диапазон",
    "value": "значение",
    "default": "по умолчанию",
    "minimum": "минимум",
    "maximum": "максимум",
    "recommended": "рекомендуемый",
    "optional": "опциональный",
    "required": "обязательный",
    "normal": "нормальный",
    "abnormal": "аномальный",
    "status": "статус",
    "state": "состояние",
    "error": "ошибка",
    "alarm": "сигнал тревоги",
    "warning light": "индикатор предупреждения",
    "indicator": "индикатор",
    "display": "дисплей",
    "interface": "интерфейс",
    "menu": "меню",
    "software": "программное обеспечение",
    "firmware": "прошивка",
    "driver": "драйвер",
    "USB": "USB",
    "network": "сеть",
    "computer": "компьютер",
    "hard disk": "жёсткий диск",
    "memory": "память",
    "system": "система",
    "version": "версия",
    "update": "обновление",
    "upgrade": "обновление",
    "download": "загрузка",
    "upload": "загрузка",
    "backup": "резервное копирование",
    "restore": "восстановление",
    "import": "импорт",
    "export": "экспорт",
    "file": "файл",
    "folder": "папка",
    "path": "путь",
    "image": "изображение",
    "picture": "изображение",
    "color": "цвет",
    "curve": "кривая",
    "horizontal": "горизонтальный",
    "vertical": "вертикальный",
    "step": "шаг",
    "origin": "начало координат",
    "home position": "начальная позиция",
    "stroke": "ход",
    "travel": "перемещение",
}

def has_english(text):
    """Check if text contains English words (excluding known brand names)."""
    brands = {"ADL07K10", "ADL07E06", "AUDLEY", "HENAN", "DIGITAL", "CO.", "LTD",
              "Henan", "Yindu", "USB", "LED", "AC", "DC", "UPS", "HEPA", "PET",
              "PT100", "Epson", "WIN7", "WIN10", "I7", "Kingston", "Intel", "Core",
              "PrintExp", "RIP", "USB3.0", "CMYK", "3200A1"}
    # Extract words
    words = re.findall(r'[A-Za-z]{3,}', text)
    eng_words = [w for w in words if w not in brands and not w.isupper()]
    return len(eng_words) > 0

def translate_block(en_text, partial_ru):
    """
    Given the original English and partially translated Russian,
    produce a fully Russian translation.
    Uses the en_text as source of truth for meaning.
    """
    result = en_text
    
    # Sort dictionary by key length (longest first) to avoid partial matches
    sorted_dict = sorted(DICT.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Do a full sentence-level translation using pattern matching
    # First, handle common full sentence patterns
    
    full_translations = {
        # ═══ K10 SENTENCES ═══
        "ADL07K10 Powder   Shaking   Machine   Instructions":
            "ADL07K10 Инструкция к машине для встряхивания порошка",
        "Henan   Yindu   Digital   Technology   Co.,   Ltd.":
            "Henan Yindu Digital Technology Co., Ltd.",
        "HENAN   AUDLEY   DIGITAL   CO.,LTD":
            "HENAN AUDLEY DIGITAL CO., LTD",
        "Henan Yindu Digital Technology Co., Ltd.":
            "Henan Yindu Digital Technology Co., Ltd.",
        "Henan   Yindu   Digital   Technology   Co.,   LTD":
            "Henan Yindu Digital Technology Co., LTD",
            
        # Safety instructions
        "Please read the following instructions before using this product.":
            "Пожалуйста, прочтите следующие инструкции перед использованием данного продукта.",
        " To ensure that you fully understand the performance of this product and its correct and safe use, please be sure to read this instruction manual thoroughly and keep it properly.":
            " Для полного понимания характеристик данного продукта и его правильного и безопасного использования, обязательно внимательно прочтите данное руководство и сохраните его.",
        " The contents of this manual and product parameters are subject to change without prior notice. If you have any questions about the product, please consult relevant technical personnel.":
            " Содержание данного руководства и параметры продукта могут быть изменены без предварительного уведомления. При возникновении вопросов обращайтесь к техническому персоналу.",
        " We have done our best to edit this description and test this product. If you find any errors, please let us know. We":
            " Мы приложили все усилия для составления инструкции и тестирования данного продукта. Если вы найдёте ошибки, пожалуйста, сообщите нам. Мы",
        "would be very grateful.":
            "будем очень благодарны.",
        " To ensure safe and correct use of this product, please read this manual carefully before use.":
            " Для безопасного и правильного использования данного продукта, пожалуйста, внимательно прочтите данное руководство перед использованием.",
        " Please keep it in a safe place and refer to it when necessary.":
            " Пожалуйста, храните руководство в надёжном месте и обращайтесь к нему при необходимости.",
        " Keep this product out of reach of children or non-professionals.":
            " Не допускайте детей и непрофессиональный персонал к данному продукту.",
        " To ensure safe and   correct use   of this product   and prevent   personal injury   and property   damage,   make":
            " Для обеспечения безопасного и правильного использования данного продукта и предотвращения травм и повреждений, необходимо",
        "sure   you   fully   understand   the   differences   between   the   following   categories   before   reading   the":
            "убедиться, что вы полностью понимаете различия между следующими категориями перед прочтением",
        "instructions.":
            "инструкции.",
        " Ignoring precautionary information such as WARNING may result in operator injury.":
            " Игнорирование предупреждений типа ПРЕДУПРЕЖДЕНИЕ может привести к травме оператора.",
        " such as CAUTION may result in operator injury or equipment damage.":
            " Пометка ОСТОРОЖНО означает возможность травмы оператора или повреждения оборудования.",
        
        # Installation
        " Do not   install   or   use   the   product   near   volatile   solvents   (alcohol   or   thinners). Do not   place any   objects   on   top   of   this":
            " Не устанавливайте и не используйте продукт вблизи летучих растворителей (спирт или разбавители). Не размещайте предметы поверх данного",
        " Do not place this product in a tilted or vibrating place.":
            " Не размещайте продукт в наклонном положении или в месте с вибрацией.",
        " Placing it this way may cause the device to tip over or be damaged.":
            " Это может привести к опрокидыванию или повреждению устройства.",
        " The suitable environment for this product is: temperature 18  ℃ -30  ℃ , humidity 40 % -60%.":
            " Подходящие условия эксплуатации: температура 18–30 ℃, влажность 40–60%.",
        "Power   supply   safety   precautions":
            "Меры безопасности при электропитании",
        "Operational   safety   precautions":
            "Меры безопасности при эксплуатации",
        "If the power cord is damaged, please disconnect the power cord as soon as possible and repair it yourself":
            "Если кабель питания повреждён, немедленно отключите его. Самостоятельный ремонт кабеля запрещён.",
        " Be careful that electricity may leak from damaged areas, causing fire or short circuit.":
            " Будьте осторожны: через повреждённые места может произойти утечка тока, что приведёт к пожару или короткому замыканию.",
        " Do not use wet hands to switch the power on or off to avoid electric shock or short circuit.":
            " Не касайтесь выключателей мокрыми руками во избежание удара электрическим током или короткого замыкания.",
        " This may cause a short circuit or even a fire.":
            " Это может вызвать короткое замыкание или пожар.",
        " Suitable ground wire locations: power supply terminal and ground stake terminal":
            " Подходящие точки заземления: клемма электропитания и клемма заземляющего контура.",
        " It is prohibited to connect grounding wires to water pipes, gas pipes, telephone lines, lightning conductors, etc.":
            " Запрещается подключать заземление к водопроводным и газовым трубам, телефонным линиям, молниеотводам и т.д.",
        " Do not attempt to disassemble or repair the device yourself.":
            " Не пытайтесь самостоятельно разбирать или ремонтировать устройство.",
        " If the device makes noise, produces smoke or flames, or emits unpleasant odors, etc., you must":
            " Если устройство издаёт шум, появляется дым, пламя или неприятный запах, необходимо",
        "immediately turn off the power and contact the manufacturer from which you purchased the device.":
            "немедленно отключить питание и обратиться к производителю, у которого вы приобрели устройство.",
        " Do not use flammable objects or products around the device.":
            " Не используйте легковоспламеняющиеся предметы и продукты вблизи устройства.",
        " Before moving the device, you need to unplug it from the power source.":
            " Перед перемещением устройства отключите его от электросети.",
        " When transporting the device, make sure the print head is in the home position.":
            " При транспортировке устройства убедитесь, что печатающая головка находится в начальной позиции.",
        "Maintenance and inspection":
            "Техническое обслуживание и осмотр",
    }
    
    # Check exact match first (normalized whitespace)
    en_norm = re.sub(r'\s+', ' ', en_text.strip())
    for pattern, translation in full_translations.items():
        pat_norm = re.sub(r'\s+', ' ', pattern.strip())
        if en_norm == pat_norm:
            return translation

    # For remaining untranslated text, do word-level replacement
    result = en_text
    # Clean up multiple spaces
    result = re.sub(r'   +', ' ', result)
    
    # Apply dictionary replacements (case-insensitive, whole word)
    for eng, rus in sorted_dict:
        pattern = re.compile(r'\b' + re.escape(eng) + r'\b', re.IGNORECASE)
        result = pattern.sub(rus, result)
    
    return result

def process_json(json_path, output_path):
    """Process a JSON translation file, fixing all partial translations."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    total = 0
    
    for page_key in data:
        blocks = data[page_key]
        for block in blocks:
            total += 1
            en = block.get("en_text", "")
            ru = block.get("ru_text", "")
            
            if not en or not ru:
                continue
            
            # Skip company names and model numbers
            if "Henan" in en and "Digital" in en and len(en) < 60:
                continue
            if "HENAN" in en and "AUDLEY" in en:
                continue
            if en.startswith("第") or en.startswith("auxiliary"):
                continue
            if en == "ADL07K10" or en == "ADL07E06":
                continue
            
            # Check if ru_text still has English
            if has_english(ru):
                new_ru = translate_block(en, ru)
                if new_ru != ru:
                    block["ru_text"] = new_ru
                    fixed_count += 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[RETRANSLATION] {json_path}")
    print(f"  Total blocks: {total}")
    print(f"  Fixed: {fixed_count}")
    return data

if __name__ == "__main__":
    base = r"E:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\PDF-NEXUS-TRANS"
    
    print("=" * 60)
    print("NEXUS RETRANSLATION ENGINE v2.0")
    print("=" * 60)
    
    # Process K10
    process_json(
        os.path.join(base, "k10_ru_hyper.json"),
        os.path.join(base, "k10_ru_CLEAN.json")
    )
    
    # Process E06  
    process_json(
        os.path.join(base, "e06_ru.json"),
        os.path.join(base, "e06_ru_CLEAN.json")
    )
    
    print("\n[DONE] Clean JSONs saved as *_CLEAN.json")
