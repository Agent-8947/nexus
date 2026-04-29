"""
NEXUS Agent 14  WIKI_COPYWRITER V2
=====================================
Специализация: Нейминг + Продающие тексты + Объяснение простым языком.

Артефакт: BRAND_IDENTITY.json
  - creative_name, slogan, sales_pitch
  - human_story: { what_it_is, who_needs_it, how_it_works, what_you_get }
  - what_to_provide: { items, note }  <- ЧТО НУЖНО ПРЕДОСТАВИТЬ
  Все разделы: EN / UA / RU
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_PROJECT_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"


class NexusCopywriterAgent:

    def __init__(self):
        print("\n" + "=" * 60)
        print("  NEXUS AGENT 14  THE CREATIVE COPYWRITER V2")
        print("  Mission: Name | Explain | Persuade | Convert")
        print("=" * 60 + "\n")

    def find_latest_build(self):
        build_dirs = []
        for domain_dir in WIKI_PROJECT_DIR.iterdir():
            if not domain_dir.is_dir():
                continue
            bp = domain_dir / "BUILD"
            if bp.exists():
                for item in bp.iterdir():
                    if item.is_dir() and (item.name.startswith("B") or "PROD_" in item.name):
                        build_dirs.append(item)
        return sorted(build_dirs)[-1] if build_dirs else None

    def read_vision(self, build_path):
        search_paths = [
            build_path,
            build_path.parent.parent,
            build_path.parent.parent / "SPEC",
        ]
        for path in search_paths:
            if not path.exists():
                continue
            for f in path.glob("*CONCEPT_*.md"):
                return f.read_text(encoding="utf-8", errors="ignore")
        return ""

    def craft_identity(self, build_path):
        print(f"[*] Analyzing: {build_path.name}")
        vision = self.read_vision(build_path)

        if "Audit" in vision or "Security" in vision:
            identity = self._build_audit_identity()
        elif "OSINT" in vision:
            identity = self._build_osint_identity()
        else:
            identity = self._build_core_identity()

        identity["agent_source"] = "14_WIKI_COPYWRITER_V2"

        out = build_path / "BRAND_IDENTITY.json"
        out.write_text(json.dumps(identity, indent=4, ensure_ascii=False), encoding="utf-8")

        print(f"  [+] Brand: '{identity['creative_name']}'")
        print(f"  [+] Slogan: {identity['slogan']}")
        print(f"  [+] Sections: story (4) + what_to_provide  EN/UA/RU")
        return identity

    #  OSINT 
    def _build_osint_identity(self):
        return {
            "creative_name": "Shadow Sight",
            "slogan": "Seeing through the digital fog of war.",
            "sales_pitch": "Total informational dominance through 4-layer autonomous reconnaissance.",
            "human_story": {
                "what_it_is": {
                    "en": "Imagine a private investigator who works 24/7, knows exactly where to look on the internet, and delivers a full dossier  without you lifting a finger.",
                    "ua": "Уявіть детектива, що працює 24/7, знає де шукати і передає повне досьє  без вашої участі.",
                    "ru": "Представьте детектива, который работает 24/7, знает где искать и передаёт полное досье  без вашего участия."
                },
                "who_needs_it": {
                    "en": "Legal professionals, journalists, due-diligence analysts  anyone who needs the full picture on a person, company, or domain before making a decision.",
                    "ua": "Юристи, журналісти, аналітики  всім, кому потрібна повна картина перед прийняттям рішення.",
                    "ru": "Юристы, журналисты, аналитики  всем, кому нужна полная картина перед принятием решения."
                },
                "how_it_works": {
                    "en": "You give it a name, domain, or email. It searches 4 intelligence layers: technical footprint, social media, leaked databases, and official registries. Everything is packaged into one clean report.",
                    "ua": "Ви даєте ім'я або домен. Система шукає в 4 шарах: технічний слід, соцмережі, витоки, реєстри. Все в одному звіті.",
                    "ru": "Вы даёте имя или домен. Система ищет по 4 слоям: технический след, соцсети, утечки, реестры. Всё в одном отчёте."
                },
                "what_you_get": {
                    "en": "A structured intelligence report that would take a human investigator several days to compile  delivered automatically in minutes.",
                    "ua": "Структурований звіт, який слідчий збирав би кілька днів  автоматично за хвилини.",
                    "ru": "Структурированный отчёт, который следователь собирал бы несколько дней  автоматически за минуты."
                }
            },
            "what_to_provide": {
                "title": {
                    "en": "What you need to give the system",
                    "ua": "Що потрібно надати системі",
                    "ru": "Что нужно передать системе"
                },
                "items": {
                    "en": [
                        "Full name of a person  (e.g.  John Smith)",
                        "OR  company name  (e.g.  Acme Corp)",
                        "OR  domain / website  (e.g.  acmecorp.com)",
                        "OR  email address  (e.g.  john@acmecorp.com)",
                        "Optional: phone number, city, known aliases"
                    ],
                    "ua": [
                        "Повне ім'я особи  (напр.  Іваненко Олександр)",
                        "АБО  назва компанії  (напр.  Acme Corp)",
                        "АБО  домен / сайт  (напр.  acmecorp.com)",
                        "АБО  e-mail адреса  (напр.  john@acmecorp.com)",
                        "Опційно: номер телефону, місто, псевдоніми"
                    ],
                    "ru": [
                        "Полное имя человека  (напр.  Иваненко Александр)",
                        "ИЛИ  название компании  (напр.  Acme Corp)",
                        "ИЛИ  домен / сайт  (напр.  acmecorp.com)",
                        "ИЛИ  e-mail адрес  (напр.  john@acmecorp.com)",
                        "Опционально: номер телефона, город, псевдонимы"
                    ]
                },
                "note": {
                    "en": "The more data you provide  the deeper and more precise the report.",
                    "ua": "Чим більше даних надаєте  тим глибший і точніший звіт.",
                    "ru": "Чем больше данных  тем глубже и точнее отчёт."
                }
            },
            "deployment": {
                "where": {
                    "en": "Runs locally on your machine  no cloud, no subscriptions, no data leaves your computer.",
                    "ua": "Запускається локально на вашому комп'ютері  жодних хмар, дані не залишають вашу машину.",
                    "ru": "Запускается локально на вашем компьютере  никаких облаков, данные не покидают машину."
                },
                "requirements": [
                    "Python 3.10+",
                    "Windows / Linux / macOS",
                    "Internet connection (for reconnaissance)",
                    "4 GB RAM minimum"
                ]
            },
            "tech_stack": {
                "label": {
                    "en": "Open-source repositories powering this tool",
                    "ua": "Відкриті репозиторії, що складають цей інструмент",
                    "ru": "Открытые репозитории, составляющие этот инструмент"
                },
                "repos": [
                    {"name": "Maigret",       "url": "github.com/soxoj/maigret",           "desc": "Username OSINT across 3000+ sites"},
                    {"name": "Holehe",        "url": "github.com/megadose/holehe",          "desc": "Email-to-accounts OSINT engine"},
                    {"name": "Sherlock",      "url": "github.com/sherlock-project/sherlock","desc": "Hunt social accounts by username"},
                    {"name": "TheHarvester", "url": "github.com/laramies/theHarvester",    "desc": "Domain emails, subdomains & IPs"},
                    {"name": "SpiderFoot",   "url": "github.com/smicallef/spiderfoot",     "desc": "Automated OSINT reconnaissance"},
                    {"name": "Subfinder",    "url": "github.com/projectdiscovery/subfinder","desc": "Passive subdomain discovery"}
                ]
            }
        }

    #  AUDIT 
    def _build_audit_identity(self):
        return {
            "creative_name": "Aegis Audit",
            "slogan": "Shielding your digital frontier with autonomous precision.",
            "sales_pitch": "A relentless, self-evolving security sentinel that never sleeps.",
            "human_story": {
                "what_it_is": {
                    "en": "Think of it as a security guard who works 24/7 and can check every door of your digital infrastructure simultaneously.",
                    "ua": "Це як охоронець, що ніколи не спить і водночас перевіряє всі цифрові входи.",
                    "ru": "Это как охранник, который никогда не спит и одновременно проверяет все цифровые входы."
                },
                "who_needs_it": {
                    "en": "Anyone who wants to know: is my infrastructure being attacked? Do I have unknown vulnerabilities?",
                    "ua": "Всім, хто хоче знати: чи є атаки на мою інфраструктуру? Чи є невідомі вразливості?",
                    "ru": "Всем, кто хочет знать: есть ли атаки на мою инфраструктуру? Есть ли неизвестные уязвимости?"
                },
                "how_it_works": {
                    "en": "It automatically scans your infrastructure on the internet, finds threats before attackers do, and delivers a structured report.",
                    "ua": "Автоматично сканує вашу інфраструктуру, знаходить загрози раніше зловмисників і формує звіт.",
                    "ru": "Автоматически сканирует инфраструктуру, находит угрозы раньше злоумышленников и формирует отчёт."
                },
                "what_you_get": {
                    "en": "A clear security picture  without hiring a security team or spending weeks on manual audits.",
                    "ua": "Чітка картина безпеки  без найму команди і ручних перевірок.",
                    "ru": "Чёткая картина безопасности  без найма команды и ручных проверок."
                }
            },
            "what_to_provide": {
                "title": {
                    "en": "What you need to give the system",
                    "ua": "Що потрібно надати системі",
                    "ru": "Что нужно передать системе"
                },
                "items": {
                    "en": [
                        "Your domain name  (e.g.  mycompany.com)",
                        "OR  IP address / server address",
                        "Optional: list of subdomains or internal services",
                        "Optional: technology stack (if known)"
                    ],
                    "ua": [
                        "Ваш домен  (напр.  mycompany.com)",
                        "АБО  IP-адреса / адреса сервера",
                        "Опційно: список піддоменів або внутрішніх сервісів",
                        "Опційно: технологічний стек (якщо відомий)"
                    ],
                    "ru": [
                        "Ваш домен  (напр.  mycompany.com)",
                        "ИЛИ  IP-адрес / адрес сервера",
                        "Опционально: список поддоменов или внутренних сервисов",
                        "Опционально: технологический стек (если известен)"
                    ]
                },
                "note": {
                    "en": "No technical knowledge required  just the domain name is enough to start.",
                    "ua": "Технічні знання не потрібні  достатньо лише доменного імені.",
                    "ru": "Технические знания не нужны  достаточно только доменного имени."
                }
            },
            "deployment": {
                "where": {
                    "en": "Runs as an autonomous background process on your local infrastructure or private server.",
                    "ua": "Працює як автономний фоновий процес на вашій локальній інфраструктурі або приватному сервері.",
                    "ru": "Работает как автономный фоновый процесс на вашей локальной инфраструктуре или частном сервере."
                },
                "requirements": [
                    "Python 3.10+",
                    "Docker (optional for isolation)",
                    "8 GB RAM for large scans"
                ]
            },
            "tech_stack": {
                "label": {
                    "en": "Open-source repositories powering this audit tool",
                    "ua": "Відкриті репозиторії, що складають цей інструмент аудиту",
                    "ru": "Открытые репозитории, составляющие этот инструмент аудита"
                },
                "repos": [
                    {"name": "Nuclei",   "url": "github.com/projectdiscovery/nuclei", "desc": "Fast and customizable vulnerability scanner"},
                    {"name": "Trivy",    "url": "github.com/aquasecurity/trivy",      "desc": "Vulnerability scanner for containers/FS"},
                    {"name": "Gitleaks", "url": "github.com/gitleaks/gitleaks",       "desc": "Protect and discover secrets"},
                    {"name": "Prowler",  "url": "github.com/prowler-cloud/prowler",   "desc": "Security tool for AWS, Azure, GCP"}
                ]
            }
        }

    #  CORE 
    def _build_core_identity(self):
        return {
            "creative_name": "Nexus Core",
            "slogan": "The heartbeat of autonomous intelligence.",
            "sales_pitch": "Unified infrastructure for next-generation data-driven decisions.",
            "human_story": {
                "what_it_is": {
                    "en": "A central command center that connects all your data sources, processes them automatically, and tells you what actually matters.",
                    "ua": "Центральний командний пункт, що збирає всі джерела і показує важливе автоматично.",
                    "ru": "Центральный командный пункт, который собирает все источники и автоматически показывает важное."
                },
                "who_needs_it": {
                    "en": "Anyone managing complex information flows who wants clear, actionable insights  without drowning in raw data.",
                    "ua": "Для тих, хто управляє складними інформаційними потоками і хоче чіткі висновки без хаосу.",
                    "ru": "Для тех, кто управляет сложными потоками данных и хочет чёткие выводы без хаоса."
                },
                "how_it_works": {
                    "en": "Data flows in from multiple sources. The system categorizes, ranks by relevance, and synthesizes into an actionable briefing.",
                    "ua": "Дані надходять з різних джерел. Система класифікує та синтезує у чіткий брифінг.",
                    "ru": "Данные поступают из разных источников. Система классифицирует и синтезирует в чёткий брифинг."
                },
                "what_you_get": {
                    "en": "Decision-ready intelligence instead of raw data chaos.",
                    "ua": "Аналітика, готова до рішень, замість хаосу сирих даних.",
                    "ru": "Аналитика, готовая к решениям, вместо хаоса сырых данных."
                }
            },
            "what_to_provide": {
                "title": {
                    "en": "What you need to give the system",
                    "ua": "Що потрібно надати системі",
                    "ru": "Что нужно передать системе"
                },
                "items": {
                    "en": [
                        "List of data sources to connect",
                        "Target domain or topic of analysis",
                        "Optional: keywords or entities to track",
                        "Optional: output format preferences (Markdown / JSON / PDF)"
                    ],
                    "ua": [
                        "Список джерел даних для підключення",
                        "Цільовий домен або тема аналізу",
                        "Опційно: ключові слова або сутності для відстеження",
                        "Опційно: бажаний формат виводу (Markdown / JSON)"
                    ],
                    "ru": [
                        "Список источников данных для подключения",
                        "Целевой домен или тема анализа",
                        "Опционально: ключевые слова или объекты для отслеживания",
                        "Опционально: желаемый формат вывода (Markdown / JSON)"
                    ]
                },
                "note": {
                    "en": "Start with just a topic or domain  the system handles the rest.",
                    "ua": "Достатньо теми або домену  система зробить усе інше.",
                    "ru": "Достаточно темы или домена  система сделает всё остальное."
                }
            },
            "deployment": {
                "where": {
                    "en": "Deploy as a master node managing specialized micro-agents.",
                    "ua": "Розгортається як майстер-вузол для управління спеціалізованими мікро-агентами.",
                    "ru": "Развёртывается как мастер-узел для управления специализированными микро-агентами."
                },
                "requirements": [
                    "Python 3.10+",
                    "Node.js 18+ (for UI)",
                    "PostgreSQL or SQLite"
                ]
            },
            "tech_stack": {
                "label": {
                    "en": "Core open-source components of the Nexus framework",
                    "ua": "Базові open-source компоненти фреймворку Nexus",
                    "ru": "Базовые open-source компоненты фреймворка Nexus"
                },
                "repos": [
                    {"name": "LangChain",    "url": "github.com/langchain-ai/langchain", "desc": "Building applications with LLMs"},
                    {"name": "FastAPI",      "url": "github.com/tiangolo/fastapi",       "desc": "High performance web framework"},
                    {"name": "Celery",       "url": "github.com/celery/celery",          "desc": "Distributed task queue"}
                ]
            }
        }


if __name__ == "__main__":
    agent = NexusCopywriterAgent()
    build = agent.find_latest_build()
    if build:
        agent.craft_identity(build)
    else:
        print("No build found.")
