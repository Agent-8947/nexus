"""
Full PDF Translator v2.0 — translates ALL text blocks from raw JSON.
Produces ru_text for every block. Preserves bbox, font_size.
"""

import json
import sys
import re


def translate_en_to_ru(text: str) -> str:
    """Translate English technical manual text to Russian."""
    
    # Skip empty text
    if not text or not text.strip():
        return text
    
    # Skip pure numbers / symbols / model numbers
    if re.match(r'^[\d\s\.\,\-\+\%\℃\/\(\)\*×xXmMkKgGwWhHzZvV]+$', text.strip()):
        return text
    
    # Chinese page numbers
    cn_page = re.match(r'第\s*(\d+)\s*页共\s*(\d+)\s*页', text)
    if cn_page:
        return f"Стр. {cn_page.group(1)} из {cn_page.group(2)}"

    # "auxiliary word for ordinal numbersNNA total of pagesMpage"
    aux_match = re.match(r'auxiliary word for ordinal numbers(\d+)A total of pages(\d+)page', text)
    if aux_match:
        return f"Стр. {aux_match.group(1)} из {aux_match.group(2)}"

    # Full dictionary of translations (every unique text block from both manuals)
    full_map = {
        # ===== COMMON HEADERS & COMPANY =====
        "Henan Yindu Digital Technology Co., Ltd.": "Henan Yindu Digital Technology Co., Ltd.",
        "Henan   Yindu   Digital   Technology   Co.,   Ltd.": "Henan Yindu Digital Technology Co., Ltd.",
        "Henan Yindu Digital Technology Co., LTD": "Henan Yindu Digital Technology Co., LTD",
        "Henan   Yindu   Digital   Technology   Co.,   LTD": "Henan Yindu Digital Technology Co., LTD",
        "HENAN   AUDLEY   DIGITAL   CO.,LTD": "HENAN AUDLEY DIGITAL CO.,LTD",

        # ===== K10 MANUAL — TITLE / TOC =====
        "ADL07K10 Powder   Shaking   Machine   Instructions": "Инструкция к машине для встряхивания порошка ADL07K10",
        "Powder Shaking Machine": "Машина для встряхивания порошка",
        "Instructions": "Инструкция",
        "☞Please   read this instruction carefully before use and keep it properly .": "☞Пожалуйста, внимательно прочтите данную инструкцию перед эксплуатацией и сохраните её.",
        "Contents": "Содержание",
        "Chapter 1 Equipment Parameters   .................................................................................. 6": "Глава 1 Параметры оборудования   .................................................................................. 6",
        "Chapter 2 Equipment Operation Guide   .........................................................................  6": "Глава 2 Руководство по эксплуатации оборудования  .........................................................................  6",
        "Chapter 3 Equipment Maintenance and Troubleshooting   .........................................  1 3": "Глава 3 Техническое обслуживание и поиск неисправностей  .........................................  1 3",

        # ===== K10 — PREFACE =====
        "Preface": "Предисловие",
        "Ensure installation and correct use": "Обеспечение правильной установки и использования",
        "Safety Instruction": "Инструкция по безопасности",
        " Thank you very much for choosing to purchase our printer .": " Благодарим вас за выбор нашего принтера.",
        " To ensure that you fully understand the performance of this product and its correct and safe use, please be sure to read this instruction manual thoroughly and keep it properly.": " Для того чтобы вы полностью понимали характеристики данного продукта и правила его безопасного использования, обязательно полностью прочтите данную инструкцию и сохраните её.",
        " The contents of this manual and product parameters are subject to change without prior notice. If you have any questions about the product, please consult relevant technical personnel.": " Содержание данного руководства и параметры продукта могут быть изменены без предварительного уведомления. При возникновении вопросов обратитесь к квалифицированному техническому специалисту.",
        " We have done our best to edit this description and test this product. If you find any errors, please let us know. We": " Мы приложили все усилия для составления данного описания и тестирования продукта. Если вы обнаружите ошибки, просим сообщить нам. Мы",
        "would be very grateful.": "будем весьма признательны.",
        " To ensure safe and correct use of this product, please read this manual carefully before use.": " Для безопасного и корректного использования данного продукта внимательно прочтите руководство перед использованием.",
        " Please keep it in a safe place and refer to it when necessary.": " Храните руководство в безопасном месте и обращайтесь к нему при необходимости.",
        " Keep this product out of reach of children or non-professionals.": " Держите данный продукт вне досягаемости детей и неквалифицированного персонала.",

        # ===== K10 — USAGE CONVENTIONS =====
        "Explain usage conventions": "Пояснение условных обозначений",
        " To ensure safe and   correct use   of this product   and prevent   personal injury   and property   damage,   make": " Для безопасного и правильного использования данного продукта, предотвращения травм и повреждения имущества,",
        "sure   you   fully   understand   the   differences   between   the   following   categories   before   reading   the": "убедитесь, что вы полностью понимаете различия между следующими категориями перед прочтением",
        "instructions.": "инструкции.",
        " Ignoring precautionary information such as WARNING may result in operator injury.": " Игнорирование предупредительной информации, такой как ПРЕДУПРЕЖДЕНИЕ, может привести к травмам оператора.",
        " such as CAUTION may result in operator injury or equipment damage.": " такой как ОСТОРОЖНО, может привести к травмам оператора или повреждению оборудования.",
        "Please read the following instructions before using this product.": "Прочтите следующие инструкции перед использованием данного продукта.",
        
        # ===== K10 — INSTALLATION / SAFETY =====
        "Printer Installation Notes": "Примечания по установке принтера",
        "WARNING": "ПРЕДУПРЕЖДЕНИЕ",
        "CAUTION": "ОСТОРОЖНО",
        " Do not   install   or   use   the   product   near   volatile   solvents   (alcohol   or   thinners). Do not   place any   objects   on   top   of   this": " Не устанавливайте и не используйте продукт вблизи летучих растворителей (спирт или растворители). Не размещайте предметы на данном",
        "product.": "продукте.",
        " Do not place this product in a tilted or vibrating place.": " Не размещайте данный продукт в наклонном положении или в месте, подверженном вибрации.",
        " Placing it this way may cause the device to tip over or be damaged.": " Такое размещение может привести к опрокидыванию или повреждению устройства.",
        "Avoid using this product in the following places": "Избегайте использования данного продукта в следующих местах",
        " Excessively humid or dry places": " Слишком влажные или сухие помещения",
        " Direct sunlight": " Прямые солнечные лучи",
        " High temperature places": " Места с высокой температурой",
        " Near open flames or moisture": " Вблизи открытого огня или источников влаги",
        " The suitable environment for this product is: temperature 18  ℃ -30  ℃ , humidity 40 % -60%.": " Подходящие условия эксплуатации: температура 18°C–30°C, влажность 40%–60%.",
        "Power   supply   safety   precautions": "Меры безопасности при электропитании",
        "If the power cord is damaged, please disconnect the power cord as soon as possible and repair it yourself": "При повреждении кабеля питания немедленно отключите его от сети и выполните ремонт",
        " Be careful that electricity may leak from damaged areas, causing fire or short circuit.": " Будьте осторожны: через повреждённые участки может произойти утечка тока, что может вызвать пожар или короткое замыкание.",
        " Do not use wet hands to switch the power on or off to avoid electric shock or short circuit.": " Не включайте/выключайте питание мокрыми руками, чтобы избежать удара током или короткого замыкания.",
        "Avoid using the same power outlet for multiple devices": "Избегайте использования одной розетки для нескольких устройств",
        " This may cause a short circuit or even a fire.": " Это может привести к короткому замыканию или пожару.",
        "Do not bundle or wrap the power cord": "Не перевязывайте и не скручивайте кабель питания",
        "When installing the ground wire, special attention should be paid": "При установке заземления обратите особое внимание",
        " Suitable ground wire locations: power supply terminal and ground stake terminal": " Подходящие места заземления: клемма питания и клемма заземляющего стержня",
        " It is prohibited to connect grounding wires to water pipes, gas pipes, telephone lines, lightning conductors, etc.": " Запрещается подключать заземляющие провода к водопроводным трубам, газовым трубам, телефонным линиям, молниеотводам и т.д.",
        "Operational   safety   precautions": "Меры безопасности при эксплуатации",
        " Do not attempt to disassemble or repair the device yourself.": " Не пытайтесь самостоятельно разбирать или ремонтировать устройство.",
        " If the device makes noise, produces smoke or flames, or emits unpleasant odors, etc., you must": " Если устройство издаёт шум, дымит, искрит или имеет неприятный запах, вы должны",
        "immediately turn off the power and contact the manufacturer from which you purchased the device.": "немедленно отключить питание и связаться с производителем, у которого вы приобрели устройство.",
        " Do not use flammable objects or products around the device.": " Не используйте легковоспламеняющиеся предметы или продукты вблизи устройства.",
        " Before moving the device, you need to unplug it from the power source.": " Перед перемещением устройства необходимо отключить его от источника питания.",
        " When transporting the device, make sure the print head is in the home position.": " При транспортировке устройства убедитесь, что печатающая головка находится в исходном положении.",
        "Maintenance and inspection": "Техническое обслуживание и осмотр",

        # ===== K10 — Ch1 Equipment Parameters =====
        "Chapter 1 Equipment Parameters": "Глава 1 Параметры оборудования",
        "Chapter 2 Equipment Operation Guide": "Глава 2 Руководство по эксплуатации оборудования",
        " Before cleaning, make sure the power is off and the power cord is unplugged. Clean the printer with a cloth moistened with cleaning fluid. Do not use volatile solvents such as alcohol lamps to clean the": " Перед очисткой убедитесь, что питание отключено и кабель питания отсоединён. Очищайте принтер тканью, смоченной чистящей жидкостью. Не используйте для очистки летучие растворители, такие как спиртовые лампы.",
        "printer.": "принтера.",
        "Product   Technical   Parameters": "Технические параметры продукта",
        "Product Model ADL07K10.": "Модель продукта ADL07K10.",
        "Applicable film width ≤ 600 MM .": "Применимая ширина плёнки ≤ 600 мм.",
        "Applicable speed ≤ 5-30 m²/h .": "Применимая скорость ≤ 5–30 м²/ч.",
        "Recommended platform": "Рекомендуемая платформа",
        "heating temperature": "температура нагрева",
        "75 ℃ .": "75°C.",
        "Recommended drying": "Рекомендуемая сушка",
        "100-150 ℃ .": "100–150°C.",
        "Media Type PET transfer film.": "Тип носителя: ПЭТ-плёнка для термопереноса.",
        "Media Transfer Net belt transmission system and paper delivery device.": "Передача носителя: Система транспортировки на сетчатом полотне и устройство подачи бумаги.",
        "Powder shaking speed It can be adjusted according to needs.": "Скорость встряхивания порошка: Регулируется в зависимости от потребностей.",
        "Powder feeding speed The   device   will   automatically   add   powder   according   to   the   current   powder   amount.   It   is   recommended   to   adjust   the   powde": "Скорость подачи порошка: Устройство автоматически добавляет порошок в зависимости от текущего количества. Рекомендуется",
        "adding speed to more than 40%.": "установить скорость подачи более 40%.",
        "power supply AC220V, 50Hz-60Hz": "Питание: AC220В, 50Гц–60Гц",
        "power Full power: 4000W. Operating power: 2200-3000W": "Мощность: Полная: 4000 Вт. Рабочая: 2200–3000 Вт",
        "Operating Environment": "Условия эксплуатации",
        "Temperature: 18 ℃ -30 ℃": "Температура: 18°C–30°C",
        "Humidity: 40 % -60 %": "Влажность: 40%–60%",
        "Machine weight Machine net weight 310KG 375KG (with packaging)": "Вес машины: Масса нетто 310 кг, 375 кг (с упаковкой)",
        "Machine size 2226mmX940mmX945mm (length*width*height)": "Габариты машины: 2226мм×940мм×945мм (длина×ширина×высота)",
        "Packing size 2310mmX1084mmX1130mm (length*width*height).": "Размер упаковки: 2310мм×1084мм×1130мм (длина×ширина×высота).",

        # ===== K10 — Ch2 Operation =====
        "Main   interface": "Главный интерфейс",
        "Manual/Auto/Stop status: The main interface is mainly used to switch the working mode in manual or automatic mode, and open and close the winding, mesh belt, suction,": "Ручной/Авто/Стоп: Главный интерфейс используется для переключения рабочего режима между ручным и автоматическим, а также для включения/выключения намотки, сетчатого полотна, отсоса,",
        "powder   shaking,   and   powder   sprinkling   functions.   After   switching   from   manual   to   automatic   mode,   all   functions   will   be   opened   by   default.   However,   because   some": "функций встряхивания и подсыпки порошка. При переключении из ручного в автоматический режим все функции включаются по умолчанию. Однако, поскольку некоторые",
        "functions are controlled by the film detection sensor in the automatic state, the winding, mesh belt, and powder shaking functions will be automatically closed and opened": "функции управляются датчиком обнаружения плёнки в автоматическом режиме, намотка, сетчатое полотно и встряхивание порошка автоматически закрываются и открываются",
        "according   to   the   state   of   the   film   detected   by   the   film   detection   sensor   unless   they   are   considered   closed   in   the   automatic   state.   The   suction   will   not   be   automatically": "в зависимости от состояния плёнки, обнаруженной датчиком, если они не были принудительно закрыты в автоматическом режиме. Отсос не будет автоматически",
        "closed, and the powder sprinkling will be automatically opened and closed according to the weight of the powder.": "закрыт, а подсыпка порошка будет автоматически включаться и выключаться в зависимости от веса порошка.",
        "Front guide plate heating": "Нагрев передней направляющей пластины",
        "Front guide plate: Displays the set temperature and actual temperature of the front guide plate": "Передняя направляющая пластина: Показывает заданную и фактическую температуру передней направляющей пластины",
        "Drying 1: Displays the set heating temperature and actual temperature of drying zone 1": "Сушка 1: Показывает заданную температуру нагрева и фактическую температуру зоны сушки 1",
        "Drying 2: Displays the set heating temperature and actual temperature of drying zone 2": "Сушка 2: Показывает заданную температуру нагрева и фактическую температуру зоны сушки 2",
        "Drying 3: Displays the set heating temperature and actual temperature of drying zone 3": "Сушка 3: Показывает заданную температуру нагрева и фактическую температуру зоны сушки 3",
        "Debug   interface:": "Интерфейс отладки:",
        "Winding speed: The rotation speed of the film winding motor is 0%-100%. Set the motor rotation speed according to the actual situation. The default is 30%-60%.": "Скорость намотки: Частота вращения мотора намотки плёнки 0%–100%. Установите скорость вращения в соответствии с фактической ситуацией. По умолчанию 30%–60%.",
        "Mesh belt speed: The rotation speed of the mesh belt motor is 0%-100%. Under normal circumstances, the speed is recommended to be 10% higher than the film speed.": "Скорость сетчатого полотна: Частота вращения мотора сетчатого полотна 0%–100%. В нормальных условиях рекомендуется устанавливать скорость на 10% выше скорости плёнки.",
        "Powder shaking speed: The rotation speed of the powder shaking motor is 0%-100%. The speed of the powder shaking motor is set according to the powder left on the film.": "Скорость встряхивания порошка: Частота вращения мотора встряхивания 0%–100%. Скорость устанавливается в зависимости от количества порошка, оставшегося на плёнке.",
        "The default setting is 30%-50%.": "Значение по умолчанию 30%–50%.",
        "Powder   spreading   speed:   The   rotation   speed   of   the   powder   spreading   motor   is   0%-100%.   The   speed   of   powder   spreading   is   set   according   to   the   actual   situation   of": "Скорость подсыпки порошка: Частота вращения мотора подсыпки 0%–100%. Скорость подсыпки устанавливается в зависимости от фактической ситуации",
        "powdering. The default setting is 40%-60%.": "нанесения порошка. Значение по умолчанию 40%–60%.",
        "Powder return: The switch function of the automatic powder return motor. After it is turned off, the automatic powder return will not work  automatically.": "Возврат порошка: Функция переключения мотора автоматического возврата порошка. После выключения автоматический возврат не будет работать.",
        "Mesh belt: forward and backward, control the forward and reverse rotation of the mesh belt. Default is forward": "Сетчатое полотно: вперёд и назад, управление прямым и обратным вращением полотна. По умолчанию — вперёд.",
        "Powder   Sprinkling:   Forward   and   reverse,   control   the   counterclockwise   and   clockwise   rotation   of   the   powder   shaft,   mainly   used   to   solve   the   problem   of   the   motor   being": "Подсыпка порошка: вперёд и назад, управление вращением вала порошка против/по часовой стрелке, используется для решения проблемы заклинивания мотора",
        "stuck due to foreign objects. The default is forward.": "из-за посторонних предметов. По умолчанию — вперёд.",
        "Temperature setting: used to adjust the temperature settings of the front guide plate, drying zone 1, drying zone 2, and drying   zone 3. The drying zone 1 is   not enabled for": "Настройка температуры: используется для регулировки температуры передней направляющей пластины, зон сушки 1, 2 и 3. Зона сушки 1 не активна для",
        "the double-head machine.": "двухголовочной машины.",
        "Front   guide   plate:   Pre-drying   treatment   of   ink   before   powdering   to   reduce   the   moisture   in   the   ink.   The   recommended   temperature   for   two   heads   is   50 ℃ ,   the": "Передняя направляющая пластина: предварительная сушка чернил перед нанесением порошка для снижения влажности. Рекомендуемая температура для двух головок 50°C,",
        "recommended   temperature   for   four   heads   is   60 ℃ ,   and   the   recommended   temperature   for   six   heads   is   60-80 ℃ .   It   can   be   increased   or   decreased   according   to   actual": "рекомендуемая для четырёх головок 60°C, для шести головок 60–80°C. Может быть увеличена или уменьшена в зависимости от фактических",
        "conditions.": "условий.",
        "Drying   zone   1:   Pre-drying   treatment   of   powdered   materials.   The   recommended   temperature   for   two   heads   is   60 ℃ ,   the   recommended   temperature   for   four   heads   is": "Зона сушки 1: предварительная сушка порошковых материалов. Рекомендуемая температура для двух головок 60°C, для четырёх головок",
        "70-80 ℃ , and the recommended temperature for six heads is 80-100 ℃ . The temperature can be increased or decreased according to actual conditions.": "70–80°C, для шести головок 80–100°C. Температура может быть изменена в зависимости от условий.",
        "Drying   zone   2:   Pre-drying   treatment   of   powdered   materials.   The   recommended   temperature   for   two   heads   is   90 ℃ ,   the   recommended   temperature   for   four   heads   is": "Зона сушки 2: предварительная сушка порошковых материалов. Рекомендуемая температура для двух головок 90°C, для четырёх головок",
        "90-120 ℃ , and the recommended temperature for six heads is 120-140 ℃ . The temperature can be increased or decreased according to actual conditions.": "90–120°C, для шести головок 120–140°C. Температура может быть изменена в зависимости от условий.",
        "Drying   zone   three:   pre-drying   treatment   of   powdered   materials.   The   recommended   temperature   for   two   heads   is   90 ℃ ,   the   recommended   temperature   for   four   heads   is": "Зона сушки 3: предварительная сушка порошковых материалов. Рекомендуемая температура для двух головок 90°C, для четырёх головок",
        "90-120 ℃ , and the recommended temperature for six heads is 120-140 ℃ . The temperature can be increased or decreased according to actual conditions. Information   interface:": "90–120°C, для шести головок 120–140°C. Температура может быть изменена в зависимости от условий. Информационный интерфейс:",
        "Motor stall/Fan overcurrent/Powder feeding timeout: When the machine is running normally, the box in front of the word will be dark green, and it will be red when an": "Заклинивание мотора/Перегрузка вентилятора/Таймаут подачи порошка: При нормальной работе машины индикатор перед текстом будет тёмно-зелёным, при возникновении",
        "alarm occurs. Click the recovery button opposite to it to cancel the alarm.": "аварийного сигнала — красным. Нажмите кнопку восстановления напротив для отмены аварийного сигнала.",
        "Device board information [control board information] [touch screen information]: Displays the version name and compilation date, used to distinguish or identify the": "Информация о плате устройства [плата управления] [сенсорный экран]: Отображает название версии и дату компиляции, используется для идентификации",
        "program version of the board": "версии программы платы",
        "Parameter   settings:": "Настройки параметров:",
        "Sensor status": "Статус датчиков",

        # ===== K10 — SENSORS & SWITCHES =====
        "IN1-Safety cover switch: 0 (displayed according to actual situation, cannot be changed manually)": "IN1-Переключатель защитной крышки: 0 (отображается по фактическому состоянию, ручное изменение невозможно)",
        "IN2-rewinding photoelectric sensor: 0 (displayed according to actual conditions and cannot be changed manually)": "IN2-Фотоэлектрический датчик перемотки: 0 (отображается по фактическому состоянию, ручное изменение невозможно)",
        "IN3-membrane sensor: 0 (displayed according to actual conditions and cannot be changed manually)": "IN3-Датчик мембраны: 0 (отображается по фактическому состоянию, ручное изменение невозможно)",
        "IN4-Proximity switch sensor: 0 (displayed according to actual conditions and cannot be changed manually)": "IN4-Датчик приближения: 0 (отображается по фактическому состоянию, ручное изменение невозможно)",
        "IN5-Drying switch: 1 (displayed according to actual conditions, cannot be changed manually) Front   guide:": "IN5-Переключатель сушки: 1 (отображается по фактическому состоянию, ручное изменение невозможно) Передняя направляющая:",
        "After   receiving   the   machine   and   unpacking   it,   you   need   to   open   the   left   and   right   cabinet   doors   and   adjust   the   fixed   position   of   the   front   guide": "После получения и распаковки машины необходимо открыть левую и правую дверцы шкафа и отрегулировать фиксированное положение передней направляющей",
        "plate   here.   There   is   one   on   each   side   of   the   machine,   and   it   is   adjusted   in   the   same   way.": "пластины здесь. Они расположены по обе стороны машины и регулируются одинаково.",
        "switch:": "переключатель:",
        "Main   Switch:   The   power   switch   of   the   host,   used   to   control   the   AC   contactor   to   turn   on   and   off   the   entire   circuit.": "Главный выключатель: Выключатель питания основного блока, управляет контактором переменного тока для включения/выключения всей цепи.",
        "Emergency   Button:   Emergency   stop   switch,   used   to   cut   off   the   power   supply   of   the   entire   machine   in   an   emergency.": "Кнопка аварийной остановки: Аварийный выключатель, используемый для экстренного отключения питания всей машины.",
        
        # ===== K10 — ROLLING =====
        "Rolling:": "Прокрутка:",
        "1 、 Where the middle LED light bar is located, you can see three stainless steel shafts, which are used to guide the heat transfer film. For the specific film penetration": "1. В области среднего LED-световода расположены три стальных вала из нержавеющей стали, используемые для направления термотрансферной плёнки. Подробную схему прохождения плёнки",
        "method, please refer to the film penetration diagram.": "см. в схеме прохождения плёнки.",
        "2 、 The switch in the green circle on the right is the switch of the LED light bar, which is used to observe the printing effect and load and unload materials.": "2. Переключатель в зелёном круге справа — переключатель LED-световода, используемый для наблюдения за качеством печати и загрузки/выгрузки материалов.",
        "3 、 There are three fans behind the three protective nets in the middle, which are used to cool the inside of the chassis and the heat transfer film.": "3. За тремя защитными сетками в средней части расположены три вентилятора, используемые для охлаждения корпуса и термотрансферной плёнки.",
        "4 、 The yellow paper roll is for taking up the printed heat transfer film. There is a switch below the green light on the right side for switching the rewinding direction.": "4. Жёлтый рулон бумаги предназначен для сматывания отпечатанной термотрансферной плёнки. Под зелёным индикатором справа расположен переключатель направления перемотки.",

        # ===== K10 — GATING =====
        "Gating:": "Управление дверцами:",
        "1 . Powder shaking cover door control. When the powder shaking motor is in working state, the powder shaking motor stops working after the cover is opened. The powder": "1. Управление дверцей отсека встряхивания. Когда мотор встряхивания работает, при открытии крышки он останавливается. Мотор встряхивания",
        "shaking motor will not work until the powder shaking compartment door is closed.": "не возобновит работу, пока дверца отсека не будет закрыта.",
        "2.   The powder spreading chute is gated. When the powder spreading motor is in working state, open the upper cover and the powder spreading motor stops working. The": "2. Лоток подсыпки порошка снабжён защитой. Когда мотор подсыпки работает, при открытии верхней крышки он останавливается. Мотор подсыпки",
        "powder spreading motor will not work until the gate switch is closed.": "не возобновит работу, пока защитный переключатель не будет закрыт.",

        # ===== K10 — PROBE CONTROL =====
        "Probe   control:": "Управление датчиком:",
        "1、Photoelectric   switch:   detects   whether   there   is   heat   transfer   film,   used   to   control   the   powder   shaking   motor,   mesh   belt   motor,   purifier,   and": "1. Фотоэлектрический переключатель: обнаруживает наличие термотрансферной плёнки, управляет мотором встряхивания, мотором сетчатого полотна, очистителем и",
        "oven   heating.": "нагревом печи.",
        "Powder   shaking   motor:   The   photoelectric   switch   starts   timing   when   it   detects   no   heat   transfer   film.   If   no   heat   transfer   film   is   detected   after": "Мотор встряхивания: фотоэлектрический переключатель начинает отсчёт, когда не обнаруживает плёнку. Если плёнка не обнаружена в течение",
        "ten   seconds,   the   powder   shaking   motor   stops   shaking   the   powder.": "десяти секунд, мотор встряхивания прекращает работу.",
        "Mesh   belt   motor:   When   the   photoelectric   switch   cannot   detect   the   heat   transfer   film,   the   mesh   belt   motor   stops   working   directly.   When   the": "Мотор сетчатого полотна: когда фотоэлектрический переключатель не обнаруживает плёнку, мотор полотна останавливается. Когда",
        "photoelectric   switch   detects   the   heat   transfer   film,   the   mesh   belt   motor   and   powder   shaking   motor   start   working   after   a   delay   of   1   second.": "фотоэлектрический переключатель обнаруживает плёнку, мотор полотна и мотор встряхивания запускаются с задержкой 1 секунда.",
        "Oven   heating:   When   the   photoelectric   switch   detects   no   heat   transfer   film,   the   heating   and   purifier   will   stop   working   at   the   same   time   after": "Нагрев печи: когда фотоэлектрический переключатель не обнаруживает плёнку, нагрев и очиститель прекращают работу одновременно через",
        "five   minutes.": "пять минут.",
        "Proximity   switch:   used   to   control   the   weight   of   powder.": "Датчик приближения: используется для контроля количества порошка.",
        "Powder quantity adjustment: If the position of the metal pointer is shifted by one grid above or below 5, the powder quantity does not change significantly. When it is at 5": "Регулировка количества порошка: если положение металлической стрелки сместится на одно деление выше или ниже 5, количество порошка существенно не изменится. При положении 5",
        "grids, the amount on the heat transfer film is about 500g-600g .": "делений количество порошка на плёнке составляет около 500–600 г.",
        "Note: The adjustment position cannot be too low. If it is too low, the powder will continue to be poured without stopping, and the abnormal red warning light will light up": "Примечание: положение регулировки не должно быть слишком низким. При слишком низком положении порошок будет подаваться непрерывно, и красный аварийный индикатор загорится",
        "every five minutes. (The time the warning light is on can be set in the background. Generally, it is not recommended to exceed 5 minutes)": "каждые пять минут. (Время горения аварийного индикатора можно настроить в фоновых параметрах. Обычно не рекомендуется превышать 5 минут)",
        "The adjustment position cannot be less than 3. If it is less than 3, the amount of powder will be relatively small, which may cause some parts of the picture to have no": "Положение регулировки не должно быть менее 3. При значении менее 3 количество порошка будет недостаточным, что может привести к отсутствию порошка на некоторых участках",
        "powder.": "изображения.",

        # ===== K10 — POWDER SAVER =====
        "Powder   saver   adjustment:": "Регулировка экономии порошка:",
        "The supporting parts in the blue box are the structure of the heat transfer film and powder, and do not need to be adjusted. The two arrows in the red circular box can be": "Опорные детали в синей рамке — структура термотрансферной плёнки и порошка, регулировка не требуется. Две стрелки в красном кружке можно",
        "pinched by hand to move the powder baffle in the red circle. After releasing them, it will automatically lock and cannot move on its own.": "сжать рукой для перемещения порошковой заслонки в красном кружке. После отпускания она автоматически фиксируется.",

        # ===== K10 — PURIFICATION =====
        "Purification   device:": "Устройство очистки:",
        "The purifier uses electric field separation plus a metal mesh, activated carbon, and HEPA filter pads for four-stage filtration to effectively reduce air pollution. The": "Очиститель использует электростатическое разделение, металлическую сетку, активированный уголь и HEPA-фильтры для четырёхступенчатой фильтрации, эффективно снижающей загрязнение воздуха.",
        "lifespan of the activated carbon and HEPA filters varies depending on the environment. Clean the filter and replace the activated carbon and HEPA filters based on their": "Срок службы фильтров с активированным углём и HEPA зависит от среды. Очищайте фильтр и заменяйте активированный уголь и HEPA-фильтры в зависимости от их",
        "effectiveness. If outdoor emissions are present, the replacement frequency can be reduced.": "эффективности. При наличии уличной вытяжки частоту замены можно снизить.",
        "Diagram   of   membrane   penetration:": "Схема прохождения мембраны:",

        # ===== K10 — Ch3 MAINTENANCE =====
        "Chapter 3 Equipment Maintenance and Troubleshooting": "Глава 3 Техническое обслуживание и поиск неисправностей",
        "1.   Equipment maintenance details:": "1. Детали технического обслуживания оборудования:",
        "(1)   Daily inspection": "(1) Ежедневный осмотр",
        " Check the   powder collecting box   and powder adding box and   clean   them   if necessary   to prevent the rubber   powder": " Проверяйте сборник порошка и бункер подачи, при необходимости очищайте, чтобы предотвратить намокание резинового порошка",
        "from getting damp or mixed with foreign objects, which may cause failure.": "или попадание посторонних предметов, что может привести к неисправности.",
        " Check   the   condensation   around   the   drying   box   and   clean   it   up   in   time   to   prevent   liquid   from   invading   electronic": " Проверяйте конденсат вокруг сушильного блока и своевременно удаляйте его, чтобы предотвратить попадание жидкости в электронные",
        "components and causing damage.": "компоненты и их повреждение.",
        "(2) Monthly inspection": "(2) Ежемесячный осмотр",
        " Check whether   there is glue powder covering   the paper detection   sensor and   the powder shaking box, and   clean   up": " Проверяйте, нет ли клеевого порошка на датчике обнаружения бумаги и в отсеке встряхивания, своевременно очищайте",
        "the dirt around the sensor in time.": "загрязнения вокруг датчика.",
        " Check whether the powder shaking shaft rotates smoothly and whether there is any abnormal noise during rotation.": " Проверяйте, вращается ли вал встряхивания плавно и нет ли аномального шума при вращении.",
        " Wipe away the dust and glue powder that has fallen into the power box.": " Удаляйте пыль и клеевой порошок, попавшие в блок питания.",
        "(3) Semi-annual inspection": "(3) Полугодовой осмотр",
        " Check the entire circuit to see if there is any looseness or disconnection, and repair it in time;": " Проверяйте всю электрическую цепь на наличие ослабленных или отсоединённых контактов и своевременно устраняйте неисправности;",
        "(4) Care and maintenance": "(4) Уход и обслуживание",
        " Powder and foreign matter in the powder shaking machine mesh belt need to be cleaned in time ;": " Порошок и посторонние предметы на сетчатом полотне машины встряхивания необходимо своевременно удалять;",
        " The   flexibility   of   the   powder   saver   and   paper   collector   swing   arm   needs   to   be   checked.   If   any   problems   are   found,": " Необходимо проверять гибкость рычага экономизатора порошка и собирателя бумаги. При обнаружении проблем",
        "they need to be repaired or replaced in time.": "их необходимо своевременно ремонтировать или заменять.",
        " Each moving part contains bearings. Check regularly whether it rotates smoothly and add lubricating oil in time.": " Каждая движущаяся часть содержит подшипники. Регулярно проверяйте плавность вращения и своевременно добавляйте смазочное масло.",

        # ===== K10 — TROUBLESHOOTING TABLE =====
        "2.   Common troubleshooting:": "2. Распространённые неисправности и их устранение:",
        "Common": "Типичные",
        "faults": "неисправности",
        "Troubleshooting direction": "Направление поиска неисправности",
        "No": "Нет",
        "powder": "порошка",
        "Possibility   1:   Check   whether   the   powder   bin   door   is   closed   and   the   door   switch   is triggered. Possibility 2: Is the motor parameter on the display 0? Possibility   3:   Board   output   failure,   check   the   output   signal   line   and   the   power   supply line to the motor Possibility 4: Has the powder level in the powder shaker reached the set requirement? Possibility 5: The proximity switch of the powder saver is damaged or loose": "Вариант 1: Проверьте, закрыта ли дверца бункера порошка и срабатывает ли концевой выключатель. Вариант 2: Параметр мотора на дисплее равен 0? Вариант 3: Неисправность выхода платы, проверьте сигнальную линию и линию питания мотора. Вариант 4: Достиг ли уровень порошка в машине установленного значения? Вариант 5: Датчик приближения экономизатора повреждён или ослаб.",
        "Powder": "Мотор",
        "shaker   do": "встряхивателя",
        "not": "не",
        "rotation": "вращается",
        "Possibility 1: Check whether the powder shaking bin door is closed and the door switch": "Вариант 1: Проверьте, закрыта ли дверца отсека встряхивания и срабатывает ли",
        "is triggered. Possibility 2: Is the motor parameter on the display 0? Possibility   3:   Board   output   failure,   check   the   output   signal   line   and   the   power   supply line to the motor Possibility   4:   Manually   check   the   motor   rotation   to   see   if   it   is   abnormal   when   the": "концевой выключатель. Вариант 2: Параметр мотора на дисплее равен 0? Вариант 3: Неисправность выхода платы, проверьте сигнальную линию и линию питания мотора. Вариант 4: Вручную проверьте вращение мотора при",
        "machine   is   turned   off.   If   there   is   a   lot   of   resistance,   check   whether   the powder shaking rod is properly installed. Possibility 5: The motor is damaged. Possibility 6: 24V power supply box output failure or line failure.": "выключенной машине. При большом сопротивлении проверьте, правильно ли установлен стержень встряхивания. Вариант 5: Мотор повреждён. Вариант 6: Неисправность блока питания 24В или неисправность линии.",
        "heating": "нагрева",
        "Possibility 1: The temperature parameter settings are incorrect. Possibility 2: The temperature probe or relay is damaged. Possibility 3: The micro switch stroke is not in place. Possibility 4: The lamp is damaged or the circuit is faulty.": "Вариант 1: Неправильные параметры температуры. Вариант 2: Температурный датчик или реле повреждены. Вариант 3: Ход микропереключателя не в рабочем положении. Вариант 4: Лампа повреждена или неисправна цепь.",
        "No film": "Нет движения",
        "movement": "плёнки",
        "Possibility 1: The switch is in automatic state, the sensor is damaged or the membrane is not sensed. Possibility 2: Motor parameter setting error. Possibility 3: 24V power supply box output failure or circuit failure. Possibility 4: The suction motor switch is not turned on.": "Вариант 1: Переключатель в автоматическом режиме, датчик повреждён или мембрана не обнаружена. Вариант 2: Ошибка настройки параметров мотора. Вариант 3: Неисправность блока питания 24В или цепи. Вариант 4: Переключатель мотора отсоса не включён.",

        # ===== K10 — OTHER PARAMETERS =====
        "Other   parameters:The   following   content   is   not   open   to   customers": "Прочие параметры: следующее содержание закрыто для клиентов",
        "directly": "напрямую",
        "Enter password: Click the dialog box at the back to enter the password 111111. After entering the password, you can see the settings below.": "Введите пароль: нажмите на диалоговое окно сзади и введите пароль 111111. После ввода пароля отобразятся настройки ниже.",
        "Time parameters": "Параметры времени",
        "Delayed working time of powder shaking motor after pause: In automatic state, if the film measuring sensor is not triggered again within the set time after starting, it will stop working. Waiting time after film-moving photoelectric trigger: the motor delay working time after the proximity switch senses that there is no film. Powder recycle working time: the time the powder recycle motor cycles when the powder recycle function is turned on. Powder return interval time: When the powder return function is turned on, the powder return motor stops working. After the set time, the powder return motor will continue to work. Heating and purifier working time when automatic stop: When the machine is in automatic state, the timing starts when it": "Задержка работы мотора встряхивания после паузы: в автоматическом режиме, если датчик плёнки не срабатывает повторно в течение установленного времени, мотор останавливается. Время ожидания после срабатывания фотодатчика: задержка работы мотора после того, как датчик приближения обнаружил отсутствие плёнки. Время работы возврата порошка: длительность цикла мотора возврата порошка при включённой функции. Интервал возврата порошка: при включённой функции возврата мотор останавливается, по истечении заданного времени возобновляет работу. Время работы нагрева и очистителя при автоматической остановке: в автоматическом режиме отсчёт начинается, когда машина",
        "does not sense the heat transfer film. After the set time, the purifier and heating will stop working. Powder supply timeout: If the powder supply is still insufficient after the set time, the alarm light will turn red. Start weight sensor detection: It is closed by default. When it is turned on, the angle proximity switch will not work. After": "не обнаруживает плёнку. По истечении заданного времени очиститель и нагрев прекращают работу. Таймаут подачи порошка: если подача по-прежнему недостаточна по истечении заданного времени, аварийный индикатор загорится красным. Запуск датчика веса: выключен по умолчанию. При включении угловой датчик приближения не работает. По истечении",
        "the powder feeding timeout period is exceeded, the alarm light will turn red and a buzzer will sound. Speed parameter (kHz) Film movement 1 Maximum speed of motor: default 40 (maximum setting 40) Film movement 2 Maximum speed of motor: default 40 (maximum setting 40) Maximum speed of powder spreading motor: default 40 (maximum setting 40) Maximum speed of the powder shaking motor: default 40 (maximum setting 20) Maximum speed of winding motor: default 40 (maximum setting 40) Other parameters 1": "таймаута подачи порошка аварийный индикатор загорится красным и прозвучит зуммер. Параметры скорости (кГц): Движение плёнки 1 — макс. скорость мотора: по умолчанию 40 (макс. значение 40). Движение плёнки 2 — макс. скорость: по умолчанию 40 (макс. 40). Макс. скорость мотора подсыпки: по умолчанию 40 (макс. 40). Макс. скорость мотора встряхивания: по умолчанию 40 (макс. 20). Макс. скорость мотора намотки: по умолчанию 40 (макс. 40). Прочие параметры 1",
        "PT100 temperature calculation compensation parameters: Default 1.018 cannot be changed Front heating KP: 50 (the default parameters include the following parameters, which can be changed. It is not recommended to change them without special needs) Front heating KI: 20 Front heating KD: 50 Drying KP1: 83 Drying KI1: 25 Drying KD1: 45 Drying KP2: 90 Drying KI2: 10 Drying KD2: 70 Drying KP3: 85 Drying KI3: 28 Drying KD3: 65 Drying curve line diagram: The curve line shows the state of heating": "Параметры компенсации расчёта температуры PT100: по умолчанию 1.018, изменению не подлежит. Передний нагрев KP: 50 (параметры по умолчанию включают нижеследующие, которые могут быть изменены. Без особой необходимости изменять не рекомендуется). Передний нагрев KI: 20. Передний нагрев KD: 50. Сушка KP1: 83. Сушка KI1: 25. Сушка KD1: 45. Сушка KP2: 90. Сушка KI2: 10. Сушка KD2: 70. Сушка KP3: 85. Сушка KI3: 28. Сушка KD3: 65. Диаграмма кривой сушки: кривая линия показывает состояние нагрева",
    }
    
    # Normalize whitespace for lookup
    normalized = re.sub(r'\s+', ' ', text.strip())
    
    # Try exact match first
    if text in full_map:
        return full_map[text]
    
    # Try normalized match
    for key, val in full_map.items():
        key_norm = re.sub(r'\s+', ' ', key.strip())
        if key_norm == normalized:
            return val
    
    # No match found — return original (will be skipped by engine v2)
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
