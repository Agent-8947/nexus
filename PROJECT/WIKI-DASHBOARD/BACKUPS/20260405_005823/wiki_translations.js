const W = {
    "en": {
        "heroTag": "Wiki Engine v1.0 — Deployed",
        "heroSub": "Complete inventory of the NEXUS knowledge ecosystem. 15 subprojects, 21 external libraries, 8 custom skills, 11 scripts, and a full documentation layer — all inside PROJECT/.",
        "s1": "15", "s1l": "Subprojects",
        "s2": "21", "s2l": "External Libraries",
        "s3": "8", "s3l": "Custom Skills",
        "s4": "11", "s4l": "Scripts",
        "s5": "5", "s5l": "Core Documents",
        "nav": ["Overview", "Projects", "Library", "Skills", "Docs", "Infra"],
        "dlBtn": "↓ Download PDF",
        "dlLoading": "Generating...",
        "dlDone": "✓ Downloaded!",

        "sec1tag": "01 — Subprojects",
        "sec1title": "Active Project Modules",
        "domains": [
            { "b": "OSINT", "h": "NEXUS-OSINT-ADVANCED", "p": "Advanced OSINT reconnaissance pipeline. Cloud enumeration, entity profiling through Maigret, Holehe, Ignorant with strict timeouts.", "t": "→ cloud_enum/ · core/ · data/ · models/" },
            { "b": "CyberThreat", "h": "NEXUS-CyberThreat-Eval", "p": "Full cyber threat evaluation framework with CLAUDE.md integration, Docker deployment, MkDocs documentation, tests, and coverage reports.", "t": "→ src/ · tests/ · reports/ · 937KB coverage" },
            { "b": "Maritime", "h": "NEXUS-MARITIME-OSINT", "p": "Maritime vessel tracking and reconnaissance. OSINT pipeline for shipping intelligence.", "t": "→ docs/" },
            { "b": "Academic", "h": "NEXUS-OSINT-ARXIV-RESEARCH", "p": "arXiv paper search, abstracts, BibTeX citations. Semantic Scholar integration for academic intelligence gathering.", "t": "→ docs/" },
            { "b": "Recon API", "h": "NEXUS-RECON-API", "p": "Unified reconnaissance API layer. Consolidates OSINT tools behind a single interface with structured output.", "t": "→ core/ · data/ · tests/ · v2/" },
            { "b": "Comms", "h": "NEXUS-FMA-BRIDGE", "p": "Financial Markets & Analytics bridge. External data connector for financial intelligence streams.", "t": "→ docs/ · dumps/" },
            { "b": "Discord", "h": "NEXUS-DISCORD-INTEL", "p": "Discord intelligence operations module. Monitoring and data extraction from Discord channels.", "t": "→ docs/" },
            { "b": "Telegram", "h": "TG-FACTORY", "p": "Telegram bot orchestration factory. Bot deployment, notification system, and automated messaging infrastructure.", "t": "→ .codex-staging · Docker · CI/CD" }
        ],

        "sec2tag": "02 — External Library",
        "sec2title": "21 Curated Repositories",
        "archCards": [
            { "b": "OSINT & Security", "h": "7 Repos", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Offensive + Defensive" },
            { "b": "Tools & Profiling", "h": "4 Repos", "p": "Maigret (username search across 2500+ sites), Holehe (email to account discovery), PhoneInfoga (phone OSINT), OpenAI-Whisper (speech-to-text).", "t": "→ Entity Profiling Stack" },
            { "b": "Engineering", "h": "6 Repos", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Learning & Architecture" },
            { "b": "Resources", "h": "4 Repos", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev.", "t": "→ API & Infra catalog" }
        ],

        "sec3tag": "03 — Custom Skills",
        "sec3title": "8 Project-Level Skills",
        "wf": [
            ["nexus-system-control", "System monitoring, bloat cleanup, Turbo Boost"],
            ["nexus-visual-motion", "Premium GSAP animations, Lenis, Three.js, shaders"],
            ["hugging-face-cli", "Full HuggingFace Hub access: models, datasets, Spaces"],
            ["nexus-migration-engine", "Architecture migration between versions"],
            ["nexus-mobile-driver", "Mobile automation and testing driver"],
            ["adversarial-reviewer", "Adversarial code and design review"],
            ["beautiful-mermaid", "Premium Mermaid diagram generation"],
            ["repo-task-proof-loop", "Task verification and proof-of-work loop"]
        ],

        "sec4tag": "04 — Documentation & Core",
        "sec4title": "Knowledge Documents",
        "skTh": ["Document", "Location", "Description"],
        "sk": [
            ["CONSTITUTION.md", "PROJECT/", "Hot Memory — architectural laws and invariants of the system"],
            ["CORE_STACK_MAP.md", "PROJECT/", "Complete technology stack mapping (6.4 KB)"],
            ["DATABASE_STACK_MAP.md", "PROJECT/", "Database layer architecture documentation (4.9 KB)"],
            ["NEXUS_SYSTEM_PROMPT.md", "PROJECT/", "System prompt definition for NEXUS agent behavior (4.4 KB)"],
            ["TECHNICAL_BRIEF.md", "DOCS/", "System technical brief and overview (3.4 KB)"],
            ["10_Ways_To_Earn.md", "DOCS/", "Monetization strategies and revenue vectors (9.3 KB)"],
            ["Mechanics_of_Earning.md", "DOCS/", "Detailed earning mechanics documentation (4.2 KB)"],
            ["Monetization_Vectors.md", "DOCS/", "Revenue stream mapping and analysis (2.2 KB)"],
            ["ENHANCEMENT_PLAN.md", "DOCS/", "System enhancement roadmap (1.5 KB)"],
            ["ASCII_DRAFTING_PROTOCOL.md", "DOCS/SPECS/", "ASCII art diagram creation standard (1.7 KB)"],
            ["SYSTEM_MAP.md", "DOCS/SPECS/", "Full system topology map (3.0 KB)"],
            ["NEXUS_JS_STANDARD.md", "STANDARDS/", "JavaScript code standard for NEXUS projects (1.5 KB)"]
        ],

        "sec5tag": "05 — Infrastructure",
        "sec5title": "Operational Layer",
        "mLabels": ["Subprojects", "Ext. Libraries", "Skills", "Scripts", "Documents", "Databases", "Configs", "Outputs"],
        "mVals": ["15", "21", "8", "11", "12", "1", "4", "3"],
        "fb1b": "Scripts", "fb1h": "11 Automation Scripts", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Infrastructure", "fb2h": "Config & Data Layer", "fb2p": "nexus_core.db (SQLite, 36KB), memory.json (6KB), fault_registry.json (2KB), mcp_config.json (5KB), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs pipeline.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v1.0 — 2026",
        "footer2": "Complete Knowledge Inventory",
        "pdfTitle": "NEXUS Wiki — Complete Knowledge Inventory",
        "pdfDate": "Generated: 2026-04-05",
        "pdfSummary": "Complete inventory of the NEXUS knowledge ecosystem: 15 subprojects, 21 external libraries, 8 custom skills, 11 scripts, 12 core documents. Zero-dependency wiki engine on pure Python stdlib."
    },
    "ru": {
        "heroTag": "Wiki Engine v1.0 — Развёрнут",
        "heroSub": "Полная инвентаризация экосистемы знаний NEXUS. 15 подпроектов, 21 внешняя библиотека, 8 кастомных скиллов, 11 скриптов и документационный слой — всё внутри PROJECT/.",
        "s1": "15", "s1l": "Подпроектов",
        "s2": "21", "s2l": "Внешних библиотек",
        "s3": "8", "s3l": "Кастомных скиллов",
        "s4": "11", "s4l": "Скриптов",
        "s5": "5", "s5l": "Ключевых документов",
        "nav": ["Обзор", "Проекты", "Библиотека", "Скиллы", "Документы", "Инфра"],
        "dlBtn": "↓ Скачать PDF",
        "dlLoading": "Генерация...",
        "dlDone": "✓ Скачано!",

        "sec1tag": "01 — Подпроекты",
        "sec1title": "Активные модули проекта",
        "domains": [
            { "b": "OSINT", "h": "NEXUS-OSINT-ADVANCED", "p": "Продвинутый OSINT-конвейер. Перечисление облачных ресурсов, профилирование через Maigret, Holehe, Ignorant.", "t": "→ cloud_enum/ · core/ · data/ · models/" },
            { "b": "КиберУгрозы", "h": "NEXUS-CyberThreat-Eval", "p": "Фреймворк оценки киберугроз с CLAUDE.md, Docker, MkDocs, тесты и отчёты покрытия.", "t": "→ src/ · tests/ · reports/ · 937KB покрытие" },
            { "b": "Морской", "h": "NEXUS-MARITIME-OSINT", "p": "Отслеживание морских судов и разведка. OSINT-конвейер для морской разведки.", "t": "→ docs/" },
            { "b": "Академический", "h": "NEXUS-OSINT-ARXIV-RESEARCH", "p": "Поиск статей arXiv, аннотации, BibTeX-цитаты. Интеграция Semantic Scholar.", "t": "→ docs/" },
            { "b": "Recon API", "h": "NEXUS-RECON-API", "p": "Единый API разведки. Консолидация OSINT-инструментов за единым интерфейсом.", "t": "→ core/ · data/ · tests/ · v2/" },
            { "b": "Финансы", "h": "NEXUS-FMA-BRIDGE", "p": "Мост финансовых рынков и аналитики. Коннектор для потоков финансовой разведки.", "t": "→ docs/ · dumps/" },
            { "b": "Discord", "h": "NEXUS-DISCORD-INTEL", "p": "Модуль разведки Discord. Мониторинг и извлечение данных из каналов.", "t": "→ docs/" },
            { "b": "Telegram", "h": "TG-FACTORY", "p": "Фабрика Telegram-ботов. Деплой ботов, уведомления и автоматизация сообщений.", "t": "→ .codex-staging · Docker · CI/CD" }
        ],

        "sec2tag": "02 — Внешняя библиотека",
        "sec2title": "21 курируемый репозиторий",
        "archCards": [
            { "b": "OSINT и безопасность", "h": "7 репозиториев", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Атака + Защита" },
            { "b": "Инструменты", "h": "4 репозитория", "p": "Maigret (поиск юзернеймов на 2500+ сайтах), Holehe (email → аккаунты), PhoneInfoga (телефонный OSINT), OpenAI-Whisper (speech-to-text).", "t": "→ Стек профилирования" },
            { "b": "Инженерия", "h": "6 репозиториев", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Обучение и архитектура" },
            { "b": "Ресурсы", "h": "4 репозитория", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev.", "t": "→ Каталог API и инфраструктуры" }
        ],

        "sec3tag": "03 — Кастомные скиллы",
        "sec3title": "8 скиллов проекта",
        "wf": [
            ["nexus-system-control", "Мониторинг, очистка, Turbo Boost"],
            ["nexus-visual-motion", "GSAP-анимации, Lenis, Three.js, шейдеры"],
            ["hugging-face-cli", "Полный доступ к HuggingFace Hub"],
            ["nexus-migration-engine", "Миграция архитектуры между версиями"],
            ["nexus-mobile-driver", "Мобильная автоматизация и тестирование"],
            ["adversarial-reviewer", "Adversarial ревью кода и дизайна"],
            ["beautiful-mermaid", "Премиальная генерация Mermaid-диаграмм"],
            ["repo-task-proof-loop", "Верификация задач и proof-of-work"]
        ],

        "sec4tag": "04 — Документация и ядро",
        "sec4title": "Документы знаний",
        "skTh": ["Документ", "Расположение", "Описание"],
        "sk": [
            ["CONSTITUTION.md", "PROJECT/", "Hot Memory — архитектурные законы и инварианты системы"],
            ["CORE_STACK_MAP.md", "PROJECT/", "Полный маппинг технологического стека (6.4 КБ)"],
            ["DATABASE_STACK_MAP.md", "PROJECT/", "Архитектура слоя баз данных (4.9 КБ)"],
            ["NEXUS_SYSTEM_PROMPT.md", "PROJECT/", "Системный промпт для поведения агента NEXUS (4.4 КБ)"],
            ["TECHNICAL_BRIEF.md", "DOCS/", "Технический обзор системы (3.4 КБ)"],
            ["10_Ways_To_Earn.md", "DOCS/", "Стратегии монетизации (9.3 КБ)"],
            ["Mechanics_of_Earning.md", "DOCS/", "Механика заработка (4.2 КБ)"],
            ["Monetization_Vectors.md", "DOCS/", "Маппинг потоков дохода (2.2 КБ)"],
            ["ENHANCEMENT_PLAN.md", "DOCS/", "Дорожная карта улучшений (1.5 КБ)"],
            ["ASCII_DRAFTING_PROTOCOL.md", "DOCS/SPECS/", "Стандарт создания ASCII-диаграмм (1.7 КБ)"],
            ["SYSTEM_MAP.md", "DOCS/SPECS/", "Полная топологическая карта системы (3.0 КБ)"],
            ["NEXUS_JS_STANDARD.md", "STANDARDS/", "JS-стандарт для проектов NEXUS (1.5 КБ)"]
        ],

        "sec5tag": "05 — Инфраструктура",
        "sec5title": "Операционный слой",
        "mLabels": ["Подпроектов", "Внеш. библ.", "Скиллов", "Скриптов", "Документов", "БД", "Конфигов", "Выходов"],
        "mVals": ["15", "21", "8", "11", "12", "1", "4", "3"],
        "fb1b": "Скрипты", "fb1h": "11 скриптов автоматизации", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Инфраструктура", "fb2h": "Конфигурация и данные", "fb2p": "nexus_core.db (SQLite, 36КБ), memory.json (6КБ), fault_registry.json (2КБ), mcp_config.json (5КБ), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v1.0 — 2026",
        "footer2": "Полная инвентаризация знаний",
        "pdfTitle": "NEXUS Wiki — Полная инвентаризация",
        "pdfDate": "Сгенерировано: 2026-04-05",
        "pdfSummary": "Полная инвентаризация экосистемы знаний NEXUS: 15 подпроектов, 21 внешняя библиотека, 8 кастомных скиллов, 11 скриптов, 12 документов. Wiki engine без зависимостей на чистом Python stdlib."
    },
    "ua": {
        "heroTag": "Wiki Engine v1.0 — Розгорнуто",
        "heroSub": "Повна інвентаризація екосистеми знань NEXUS. 15 підпроектів, 21 зовнішня бібліотека, 8 кастомних скілів, 11 скриптів і документаційний шар — усе всередині PROJECT/.",
        "s1": "15", "s1l": "Підпроектів",
        "s2": "21", "s2l": "Зовнішніх бібліотек",
        "s3": "8", "s3l": "Кастомних скілів",
        "s4": "11", "s4l": "Скриптів",
        "s5": "5", "s5l": "Ключових документів",
        "nav": ["Огляд", "Проекти", "Бібліотека", "Скіли", "Документи", "Інфра"],
        "dlBtn": "↓ Завантажити PDF",
        "dlLoading": "Генерація...",
        "dlDone": "✓ Завантажено!",

        "sec1tag": "01 — Підпроекти",
        "sec1title": "Активні модулі проекту",
        "domains": [
            { "b": "OSINT", "h": "NEXUS-OSINT-ADVANCED", "p": "Просунутий OSINT-конвеєр. Перерахування хмар, профілювання через Maigret, Holehe, Ignorant.", "t": "→ cloud_enum/ · core/ · data/ · models/" },
            { "b": "КіберЗагрози", "h": "NEXUS-CyberThreat-Eval", "p": "Фреймворк оцінки кіберзагроз з CLAUDE.md, Docker, MkDocs, тести та звіти покриття.", "t": "→ src/ · tests/ · reports/ · 937KB покриття" },
            { "b": "Морський", "h": "NEXUS-MARITIME-OSINT", "p": "Відстеження морських суден та розвідка.", "t": "→ docs/" },
            { "b": "Академічний", "h": "NEXUS-OSINT-ARXIV-RESEARCH", "p": "Пошук статей arXiv, анотації, BibTeX-цитати. Інтеграція Semantic Scholar.", "t": "→ docs/" },
            { "b": "Recon API", "h": "NEXUS-RECON-API", "p": "Єдиний API розвідки. Консолідація OSINT-інструментів за єдиним інтерфейсом.", "t": "→ core/ · data/ · tests/ · v2/" },
            { "b": "Фінанси", "h": "NEXUS-FMA-BRIDGE", "p": "Міст фінансових ринків та аналітики.", "t": "→ docs/ · dumps/" },
            { "b": "Discord", "h": "NEXUS-DISCORD-INTEL", "p": "Модуль розвідки Discord. Моніторинг та витягування даних з каналів.", "t": "→ docs/" },
            { "b": "Telegram", "h": "TG-FACTORY", "p": "Фабрика Telegram-ботів. Деплой, повідомлення та автоматизація.", "t": "→ .codex-staging · Docker · CI/CD" }
        ],

        "sec2tag": "02 — Зовнішня бібліотека",
        "sec2title": "21 курований репозиторій",
        "archCards": [
            { "b": "OSINT та безпека", "h": "7 репозиторіїв", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Атака + Захист" },
            { "b": "Інструменти", "h": "4 репозиторії", "p": "Maigret (пошук юзернеймів на 2500+ сайтах), Holehe (email → акаунти), PhoneInfoga (телефонний OSINT), OpenAI-Whisper.", "t": "→ Стек профілювання" },
            { "b": "Інженерія", "h": "6 репозиторіїв", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Навчання та архітектура" },
            { "b": "Ресурси", "h": "4 репозиторії", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev.", "t": "→ Каталог API та інфраструктури" }
        ],

        "sec3tag": "03 — Кастомні скіли",
        "sec3title": "8 скілів проекту",
        "wf": [
            ["nexus-system-control", "Моніторинг, очищення, Turbo Boost"],
            ["nexus-visual-motion", "GSAP-анімації, Lenis, Three.js, шейдери"],
            ["hugging-face-cli", "Повний доступ до HuggingFace Hub"],
            ["nexus-migration-engine", "Міграція архітектури між версіями"],
            ["nexus-mobile-driver", "Мобільна автоматизація та тестування"],
            ["adversarial-reviewer", "Adversarial рев'ю коду та дизайну"],
            ["beautiful-mermaid", "Преміальна генерація Mermaid-діаграм"],
            ["repo-task-proof-loop", "Верифікація задач та proof-of-work"]
        ],

        "sec4tag": "04 — Документація та ядро",
        "sec4title": "Документи знань",
        "skTh": ["Документ", "Розташування", "Опис"],
        "sk": [
            ["CONSTITUTION.md", "PROJECT/", "Hot Memory — архітектурні закони та інваріанти системи"],
            ["CORE_STACK_MAP.md", "PROJECT/", "Повний маппінг технологічного стеку (6.4 КБ)"],
            ["DATABASE_STACK_MAP.md", "PROJECT/", "Архітектура шару баз даних (4.9 КБ)"],
            ["NEXUS_SYSTEM_PROMPT.md", "PROJECT/", "Системний промпт для поведінки агента (4.4 КБ)"],
            ["TECHNICAL_BRIEF.md", "DOCS/", "Технічний огляд системи (3.4 КБ)"],
            ["10_Ways_To_Earn.md", "DOCS/", "Стратегії монетизації (9.3 КБ)"],
            ["Mechanics_of_Earning.md", "DOCS/", "Механіка заробітку (4.2 КБ)"],
            ["Monetization_Vectors.md", "DOCS/", "Маппінг потоків доходу (2.2 КБ)"],
            ["ENHANCEMENT_PLAN.md", "DOCS/", "Дорожня карта покращень (1.5 КБ)"],
            ["ASCII_DRAFTING_PROTOCOL.md", "DOCS/SPECS/", "Стандарт ASCII-діаграм (1.7 КБ)"],
            ["SYSTEM_MAP.md", "DOCS/SPECS/", "Повна топологічна карта системи (3.0 КБ)"],
            ["NEXUS_JS_STANDARD.md", "STANDARDS/", "JS-стандарт для проектів NEXUS (1.5 КБ)"]
        ],

        "sec5tag": "05 — Інфраструктура",
        "sec5title": "Операційний шар",
        "mLabels": ["Підпроектів", "Зовн. бібл.", "Скілів", "Скриптів", "Документів", "БД", "Конфігів", "Виходів"],
        "mVals": ["15", "21", "8", "11", "12", "1", "4", "3"],
        "fb1b": "Скрипти", "fb1h": "11 скриптів автоматизації", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Інфраструктура", "fb2h": "Конфігурація та дані", "fb2p": "nexus_core.db (SQLite, 36КБ), memory.json (6КБ), fault_registry.json (2КБ), mcp_config.json (5КБ), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v1.0 — 2026",
        "footer2": "Повна інвентаризація знань",
        "pdfTitle": "NEXUS Wiki — Повна інвентаризація",
        "pdfDate": "Згенеровано: 2026-04-05",
        "pdfSummary": "Повна інвентаризація екосистеми знань NEXUS: 15 підпроектів, 21 зовнішня бібліотека, 8 кастомних скілів, 11 скриптів, 12 документів."
    }
};
