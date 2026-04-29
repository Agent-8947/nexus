const W = {
    "en": {
        "heroTag": "Wiki Engine v6.0 — Hardened",
        "heroSub": "Complete inventory of the NEXUS knowledge ecosystem. 1491 Knowledge Nodes, 32 Autonomous Agents, 34 Custom Skills, 45 Automation Scripts, and 30 Precision Workflows.",
        "s1": "15", "s1l": "Subprojects",
        "s2": "1491", "s2l": "Knowledge Nodes",
        "s3": "34", "s3l": "NEXUS Skills",
        "s4": "32", "s4l": "Wiki Agents",
        "s5": "30", "s5l": "Workflows",
        "nav": ["Overview", "Agents", "Projects", "Nodes", "Skills", "Docs", "Infra"],
        "dlBtn": "↓ Download PDF",
        "dlLoading": "Generating...",
        "dlDone": "✓ Downloaded!",

        "sec6tag": "00 — The Agent Roster",
        "sec6title": "32 Synthesized Wiki Agents",
        "ag": [
            ["WIKI_BRAIN", "Central logic repository"], ["WIKI_PRIME", "Nexus system initializer"], ["BULK_INGESTOR", "Mass knowledge loader"], ["WIKI_AUTOPILOT", "Autonomous mode controller"],
            ["WIKI_ARCHIVIST", "Knowledge cataloging expert"], ["WIKI_FUSION", "Agent DNA synthesis engine"], ["WIKI_ENGINEER", "Core architecture and coding"], ["WIKI_OSINT", "Strategic reconnaissance expert"],
            ["ENGINEER_CLOUD", "Cloud infrastructure manager"], ["WIKI_RESEARCHER", "Deep research and fact-check"], ["TECHNICAL_VISION", "System design and visioning"], ["FUSION_INTEGRATOR", "Synthesis finalization"],
            ["WIKI_CONSTRUCTOR", "Modular assembly specialist"], ["WIKI_SORTER", "Content categorization logic"], ["WIKI_MARKETER", "Packaging and presentation"], ["WIKI_COPYWRITER", "Content generation engine"],
            ["WIKI_DEPLOYER", "Deployment orchestration"], ["WIKI_VALIDATOR", "Code verification and QA"], ["GITHUB_PROFILE", "Auth and profile management"], ["WIKI_LEGISLATOR", "Standard enforcement"],
            ["WIKI_COMPOUNDER", "Resource multiplication"], ["WIKI_PHILOSOPHER", "Conceptual and ethics logic"], ["ORCHESTRATOR", "Agent swarm coordinator"], ["NEXUS_AUTO_FARM", "Repo farm manager"],
            ["INFINITE_LOOP", "Cyclic analysis engine"], ["QWEN_FARMER", "LLM optimization specialist"], ["DESIGN_EYE", "UI/UX review specialist"], ["EVOLUTION_MASTER", "Agent training and growth"],
            ["LOGIC_EVOLVER", "Mutation and AST evolving"], ["FARM_BUILDER", "Infrastructure setup"], ["DOMAIN_MAP_GEN", "Network topology mapping"], ["run_agent", "Unified agent loader"]
        ],

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
            { "b": "Telegram", "h": "TG-FACTORY", "p": "Telegram bot orchestration factory. Bot deployment, notification system, and automated messaging infrastructure.", "t": "→ .codex-staging · Docker · CI/CD" },
            { "b": "Synthesis", "h": "WIKI-AGENT", "p": "The core of autonomous intelligence. Managing 1491 knowledge nodes and synthesizing new agent DNA.", "t": "→ logic_evolver/ · dna_factory/ · 32 agents" },
            { "b": "Pipeline", "h": "NEXUS-PIPELINE-V3", "p": "Massive orchestration bus. Connecting all subprojects into a single autonomous execution loop.", "t": "→ core/ · flows/ · tasks/" }
        ],

        "sec2tag": "02 — Knowledge Base",
        "sec2title": "1491 Validated Nodes",
        "archCards": [
            { "b": "OSINT & Security", "h": "7 Repos", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Offensive + Defensive" },
            { "b": "Tools & Profiling", "h": "4 Repos", "p": "Maigret (username search across 2500+ sites), Holehe (email to account discovery), PhoneInfoga (phone OSINT), OpenAI-Whisper (speech-to-text).", "t": "→ Entity Profiling Stack" },
            { "b": "Engineering", "h": "6 Repos", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Learning & Architecture" },
            { "b": "Resources", "h": "5 Repos", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev, Free-Programming-Books.", "t": "→ API & Infra catalog" }
        ],

        "sec3tag": "03 — Autonomous Intelligence",
        "sec3title": "32 Wiki Agents & 34 Skills",
        "wf": [
            ["answering-engine", "Deep AI research engine"], ["api-schema-enforcer", "API contract sentinel"], ["arxiv-research", "Academic paper intelligence"], ["blockchain-auditor", "Smart contract safety"],
            ["cloud-finops", "Cloud cost optimization"], ["codebase-inspection", "Repo audit & statistics"], ["context-manager", "Session memory architecture"], ["cyber-intel", "Threat intel aggregation"],
            ["data-lake", "Data lifecycle management"], ["database-shard", "Distributed scaling"], ["domain-intel", "Passive reconnaissance"], ["firecrawl", "Advanced web scraping"],
            ["frontend-orch", "Visual system control"], ["git-native", "Git-agent specification"], ["github-pr", "Full PR automation"], ["hunchly-intel", "Evidence collection"],
            ["justdoit", "Task execution loops"], ["knowledge-synth", "Data into DNA conversion"], ["legal-compliance", "Regulatory checking"], ["mathlib-advisor", "Mathematical validation"],
            ["motion-design", "Premium web animations"], ["agent-orch", "Swarm delegation engine"], ["botnet-hunter", "Internal node monitor"], ["deploy-architect", "Server config orchestrator"],
            ["legal-notary", "Compliance verification"], ["nexus-qa", "Agentic browser testing"], ["nexus-vision", "Product-market fit AI"], ["osint-tactician", "Recon strategy engine"],
            ["powershell-ui", "Desktop GUI architecture"], ["redteam-pentest", "Adversarial simulations"], ["security-audit", "Advanced defense system"], ["state-anomaly", "Logic monitoring agent"],
            ["ui-ux-designer", "Premium design architect"], ["zero-trust", "Identity broker"]
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
        "mLabels": ["Subprojects", "Knowledge Nodes", "Skills", "Agents", "Documents", "Workflows", "Scripts", "Outputs"],
        "mVals": ["15", "1491", "34", "32", "12", "30", "45", "3"],
        "fb1b": "Scripts", "fb1h": "11 Automation Scripts", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Infrastructure", "fb2h": "Config & Data Layer", "fb2p": "nexus_core.db (SQLite, 36KB), memory.json (6KB), fault_registry.json (2KB), mcp_config.json (5KB), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs pipeline.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v6.0 — 2026",
        "footer2": "Precision Intelligence Log",
        "pdfTitle": "NEXUS Wiki — Intelligence Atlas",
        "pdfDate": "Generated: 2026-04-21",
        "pdfSummary": "Complete inventory of the NEXUS knowledge ecosystem: 15 subprojects, 1491 knowledge nodes, 32 agents, 34 custom skills, 45 automation scripts. Autonomous Intelligence Pipeline."
    },
    "ru": {
        "heroTag": "Wiki Engine v6.0 — Развёрнут",
        "heroSub": "Полная инвентаризация экосистемы знаний NEXUS. 1491 узел знаний, 32 автономных агента, 34 кастомных скилла, 30 воркфлоу — всё внутри PROJECT/.",
        "s1": "15", "s1l": "Подпроектов",
        "s2": "1491", "s2l": "Узлов знаний",
        "s3": "34", "s3l": "NEXUS Скиллов",
        "s4": "32", "s4l": "Wiki Агентов",
        "s5": "30", "s5l": "Воркфлоу",
        "nav": ["Обзор", "Агенты", "Проекты", "Узлы", "Скиллы", "Документы", "Инфра"],
        "dlBtn": "↓ Скачать PDF",
        "dlLoading": "Генерация...",
        "dlDone": "✓ Скачано!",

        "sec6tag": "00 — Список Агентов",
        "sec6title": "32 синтезированных Wiki-агента",
        "ag": [
            ["WIKI_BRAIN", "Центральное хранилище логики"], ["WIKI_PRIME", "Инициализатор системы Nexus"], ["BULK_INGESTOR", "Массовая загрузка знаний"], ["WIKI_AUTOPILOT", "Контроллер автопилота"],
            ["WIKI_ARCHIVIST", "Эксперт по каталогизации"], ["WIKI_FUSION", "Синтез ДНК новых агентов"], ["WIKI_ENGINEER", "Ядро архитектуры и кода"], ["WIKI_OSINT", "Стратегическая разведка"],
            ["ENGINEER_CLOUD", "Облачная инфраструктура"], ["WIKI_RESEARCHER", "Глубокий поиск и фактчекинг"], ["TECHNICAL_VISION", "Техническое видение и дизайн"], ["FUSION_INTEGRATOR", "Финализация синтеза"],
            ["WIKI_CONSTRUCTOR", "Специалист по сборке"], ["WIKI_SORTER", "Категоризация контента"], ["WIKI_MARKETER", "Упаковка и презентация"], ["WIKI_COPYWRITER", "Генерация контента"],
            ["WIKI_DEPLOYER", "Оркестрация развертывания"], ["WIKI_VALIDATOR", "Верификация кода и QA"], ["GITHUB_PROFILE", "Управление профилями GitHub"], ["WIKI_LEGISLATOR", "Контроль стандартов"],
            ["WIKI_COMPOUNDER", "Умножение ресурсов"], ["WIKI_PHILOSOPHER", "Концептуальная логика"], ["ORCHESTRATOR", "Координатор роя агентов"], ["NEXUS_AUTO_FARM", "Управление фермой репо"],
            ["INFINITE_LOOP", "Циклический анализ"], ["QWEN_FARMER", "Оптимизация LLM (Qwen)"], ["DESIGN_EYE", "Ревьюер UI/UX дизайна"], ["EVOLUTION_MASTER", "Развитие и рост агентов"],
            ["LOGIC_EVOLVER", "Эволюция логики и AST"], ["FARM_BUILDER", "Настройка инфраструктуры"], ["DOMAIN_MAP_GEN", "Картирование сети"], ["run_agent", "Универсальный загрузчик"]
        ],

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
            { "b": "Telegram", "h": "TG-FACTORY", "p": "Фабрика Telegram-ботов. Деплой ботов, уведомления и автоматизация сообщений.", "t": "→ .codex-staging · Docker · CI/CD" },
            { "b": "Синтез", "h": "WIKI-AGENT", "p": "Ядро автономного интеллекта. Управление 1491 узлами знаний и синтез новых ДНК агентов.", "t": "→ logic_evolver/ · dna_factory/ · 32 агента" },
            { "b": "Пайплайн", "h": "NEXUS-PIPELINE-V3", "p": "Магистраль оркестрации. Соединяет все подпроекты в единый цикл автономного исполнения.", "t": "→ core/ · flows/ · tasks/" }
        ],

        "sec2tag": "02 — База знаний",
        "sec2title": "1491 верифицированный узел",
        "archCards": [
            { "b": "OSINT и безопасность", "h": "7 репозиториев", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Атака + Защита" },
            { "b": "Инструменты", "h": "4 репозитория", "p": "Maigret (поиск юзернеймов на 2500+ сайтах), Holehe (email → аккаунты), PhoneInfoga (телефонный OSINT), OpenAI-Whisper (speech-to-text).", "t": "→ Стек профилирования" },
            { "b": "Инженерия", "h": "6 репозиториев", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Обучение и архитектура" },
            { "b": "Ресурсы", "h": "5 репозиториев", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev, Free-Programming-Books.", "t": "→ Каталог API и инфраструктуры" }
        ],

        "sec3tag": "03 — Автономный Интеллект",
        "sec3title": "32 Wiki-агента и 34 Скилла",
        "wf": [
            ["answering-engine", "Глубокий AI-поиск и верификация"], ["api-schema-enforcer", "Контроль контрактов API"], ["arxiv-research", "Академическая разведка ArXiv"], ["blockchain-auditor", "Безопасность смарт-контрактов"],
            ["cloud-finops", "Оптимизация облачных затрат"], ["codebase-inspection", "Аудит и статистика репозиториев"], ["context-manager", "Архитектура памяти сессий"], ["cyber-intel", "Агрегация киберугроз"],
            ["data-lake", "Управление жизненным циклом данных"], ["database-shard", "Распределенное масштабирование"], ["domain-intel", "Пассивная разведка доменов"], ["firecrawl", "Продвинутый скрапинг веба"],
            ["frontend-orch", "Визуальное управление системой"], ["git-native", "Спецификация Git-агентов"], ["github-pr", "Автоматизация PR в GitHub"], ["hunchly-intel", "Сбор цифровых доказательств"],
            ["justdoit", "Циклы исполнения задач"], ["knowledge-synth", "Конвертация данных в ДНК"], ["legal-compliance", "Проверка на соответствие праву"], ["mathlib-advisor", "Математическая валидация"],
            ["motion-design", "Премиальная веб-анимация"], ["agent-orch", "Оркестрация роя агентов"], ["botnet-hunter", "Мониторинг внутренних узлов"], ["deploy-architect", "Конфигурация серверов"],
            ["legal-notary", "Верификация комплаенса"], ["nexus-qa", "Агентское тестирование браузера"], ["nexus-vision", "AI-анализ соответствия рынку"], ["osint-tactician", "Стратегия разведки"],
            ["powershell-ui", "Архитектура десктопного GUI"], ["redteam-pentest", "Атакующие симуляции"], ["security-audit", "Продвинутая система защиты"], ["state-anomaly", "Мониторинг логики системы"],
            ["ui-ux-designer", "Проектирование премиум-дизайна"], ["zero-trust", "Брокер идентификации"]
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
        "mLabels": ["Подпроектов", "Узлов знаний", "Скиллов", "Агентов", "Документов", "Воркфлоу", "Скриптов", "Выходов"],
        "mVals": ["15", "1491", "34", "32", "12", "30", "45", "3"],
        "fb1b": "Скрипты", "fb1h": "11 скриптов автоматизации", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Инфраструктура", "fb2h": "Конфигурация и данные", "fb2p": "nexus_core.db (SQLite, 36КБ), memory.json (6КБ), fault_registry.json (2КБ), mcp_config.json (5КБ), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v6.0 — 2026",
        "footer2": "Атлас Интеллекта",
        "pdfTitle": "NEXUS Wiki — Атлас Знаний",
        "pdfDate": "Сгенерировано: 2026-04-21",
        "pdfSummary": "Полная инвентаризация экосистемы знаний NEXUS: 15 подпроектов, 1491 узел знаний, 32 агента, 34 кастомных скилла, 45 скриптов. Автономный конвейер интеллекта."
    },
    "ua": {
        "heroTag": "Wiki Engine v1.0 — Розгорнуто",
        "heroSub": "Повна інвентаризація екосистеми знань NEXUS. 15 підпроектів, 21 зовнішня бібліотека, 8 кастомних скілів, 11 скриптів і документаційний шар — усе всередині PROJECT/.",
        "s1": "15", "s1l": "Підпроектів",
        "s2": "22", "s2l": "Зовнішніх бібліотек",
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
        "sec2title": "22 куровані репозиторії",
        "archCards": [
            { "b": "OSINT та безпека", "h": "7 репозиторіїв", "p": "Awesome-OSINT, Awesome-Hacking, Awesome-Pentest, Awesome-Web-Security, PayloadsAllTheThings, The-Book-of-Secret-Knowledge, social-engineer-toolkit.", "t": "→ Атака + Захист" },
            { "b": "Інструменти", "h": "4 репозиторії", "p": "Maigret (пошук юзернеймів на 2500+ сайтах), Holehe (email → акаунти), PhoneInfoga (телефонний OSINT), OpenAI-Whisper.", "t": "→ Стек профілювання" },
            { "b": "Інженерія", "h": "6 репозиторіїв", "p": "Build-Your-Own-X, System-Design-Primer, Developer-Roadmap, TheAlgorithms-Python, DevOps-Exercises, awesome-testing.", "t": "→ Навчання та архітектура" },
            { "b": "Ресурси", "h": "5 репозиторіїв", "p": "Awesome-Python, Awesome-Selfhosted, Public-APIs, Free-For-Dev, Free-Programming-Books.", "t": "→ Каталог API та інфраструктури" }
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
        "mVals": ["15", "22", "8", "11", "12", "1", "4", "3"],
        "fb1b": "Скрипти", "fb1h": "11 скриптів автоматизації", "fb1p": "freeze_nexus.py, toolkit_enrichment.py, toolkit_localization.py, toolkit_parser.py, toolkit_slugger.py, record_hero_video.py, record_hero_mobile_video.py, replicate_nexus.py, nexus_knowledge_ingest.py, send_monetization_email.py, auth_gmail.py.", "fb1t": "→ PROJECT/scripts/ · PROJECT/",
        "fb2b": "Інфраструктура", "fb2h": "Конфігурація та дані", "fb2p": "nexus_core.db (SQLite, 36КБ), memory.json (6КБ), fault_registry.json (2КБ), mcp_config.json (5КБ), docker-compose.yml, .env, .env.mcp. Apache Airflow DAGs.", "fb2t": "→ Production Ready · Airflow DAGs",

        "footer1": "NEXUS Wiki Engine v1.0 — 2026",
        "footer2": "Повна інвентаризація знань",
        "pdfTitle": "NEXUS Wiki — Повна інвентаризація",
        "pdfDate": "Згенеровано: 2026-04-05",
        "pdfSummary": "Повна інвентаризація екосистеми знань NEXUS: 15 підпроектів, 22 зовнішня бібліотека, 8 кастомних скілів, 11 скриптів, 12 документів."
    }
};
