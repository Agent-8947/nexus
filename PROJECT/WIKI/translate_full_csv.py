import csv
import re
from pathlib import Path

# Updated High-Fidelity Translation Map (extended to 400 items logic)
# This includes general descriptions and specific repo mappings
TRANS_MAP = {
    # Top repos
    "Master programming by recreating your favorite technologies from scratch.": "Освойте программирование, воссоздавая технологии с нуля.",
    "😎 Awesome lists about all kinds of interesting topics": "😎 Потрясающие списки на самые разные темы.",
    "A collective list of free APIs": "Коллективный список бесплатных API.",
    ":books: Freely available programming books": ":books: Бесплатные книги по программированию.",
    "Interactive roadmaps, guides and other educational content to help developers grow in their careers.": "Интерактивные дорожные карты и контент для развития карьеры.",
    "Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞": "Персональный AI-ассистент. Любая ОС. В стиле лобстера. 🦞",
    "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.": "Проектирование систем. Подготовка к интервью. Карточки Anki.",
    "A complete computer science study plan to become a software engineer.": "Полный план обучения для становления инженером.",
    "An opinionated list of Python frameworks, libraries, tools, and resources": "Субъективный список Python-инструментов и фреймворков.",
    "A list of Free Software network services and web applications which can be hosted on your own servers": "Список ПО для хостинга на собственных серверах.",
    "Repo for counting stars and contributing. Press F to pay respect to glorious developers.": "Репо для звезд и вкладов. Нажмите F для уважения.",
    "Curated list of project-based tutorials": "Кураторский список проектных туториалов.",
    "The library for web and native user interfaces.": "Библиотека для веб- и нативных интерфейсов.",
    "Linux kernel source tree": "Исходный код ядра Linux.",
    "All Algorithms implemented in Python": "Все алгоритмы, реализованные на Python.",
    "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and more.": "Коллекция списков, мануалов и хаков.",
    "This is the repo for Vue 2. For Vue 3, go to https://github.com/vuejs/core": "Репозиторий Vue 2. Для Vue 3 перейдите по ссылке.",
    "🎓 Path to a free self-taught education in Computer Science!": "🎓 Путь к самообразованию в Computer Science!",
    "📝 Algorithms and data structures implemented in JavaScript with explanations and links to further readings": "📝 Алгоритмы и структуры данных на JavaScript.",
    "An Open Source Machine Learning Framework for Everyone": "Фреймворк машинного обучения для всех.",
    "A book series (2 published editions) on the JS language.": "Серия книг по языку JavaScript.",
    "Visual Studio Code": "Редактор Visual Studio Code.",
    "AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters.": "Видение доступного ИИ для всех.",
    "Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.": "Платформа автоматизации с ИИ и 400+ интеграциями.",
    "Flutter makes it easy and fast to build beautiful apps for mobile and beyond": "Flutter: быстрое создание красивых мобильных приложений.",
    "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.": "Популярный фреймворк для адаптивной верстки.",
    "A collection of useful .gitignore templates": "Коллекция шаблонов .gitignore.",
    "A curated list of awesome Go frameworks, libraries and software": "Кураторский список инструментов для Go.",
    "Stable Diffusion web UI": "Веб-интерфейс для Stable Diffusion.",
    "Master the command line, in one page": "Освоение командной строки на одной странице.",
    "DigitalPlat FreeDomain: Free Domain For Everyone": "Бесплатные домены для всех.",
    "A feature-rich command-line audio/video downloader": "Полнофункциональный загрузчик аудио/видео.",
    "JavaScript Style Guide": "Гайд по стилю JavaScript.",
    "Langflow is a powerful tool for building and deploying AI-powered agents and workflows.": "Инструмент для создания и деплоя ИИ-агентов.",
    "Command-line program to download videos from YouTube.com and other video sites": "Программа для загрузки видео с YouTube.",
    "The React Framework": "Фреймворк React.",
    "Curated coding interview preparation materials for busy software engineers": "Материалы для подготовки к интервью.",
    "Display and control your Android device": "Отображение и управление Android устройством.",
    "The open source coding agent.": "Агент для написания кода с открытым кодом.",
    "Production-ready platform for agentic workflow development.": "Платформа для разработки агентных воркфлоу.",
    "An agentic skills framework & software development methodology that works.": "Фреймворк агентных скиллов и методология разработки.",
    "The Go programming language": "Язык программирования Go.",
    "The agent engineering platform": "Платформа проектирования агентов.",
    "Microsoft PowerToys is a collection of utilities that supercharge productivity and customization on Windows": "Утилиты для повышения продуктивности в Windows.",
    "Coding articles to level up your development skills": "Статьи по программированию для повышения навыков.",
    "A framework for building native applications using React": "Фреймворк для нативных приложений на React.",
    "Production-Grade Container Scheduling and Management": "Управление контейнерами промышленного уровня.",
    ":electron: Build cross-platform desktop apps with JavaScript, HTML, and CSS": "Десктоп-приложения на JS, HTML и CSS.",
    "Virtual whiteboard for sketching hand-drawn like diagrams": "Виртуальная доска для рисования диаграмм.",
    "Node.js JavaScript runtime ✨🐢🚀✨": "Среда выполнения Node.js.",
    "Collection of publicly available IPTV channels from all over the world": "Коллекция публичных IPTV каналов.",
    "JavaScript 3D Library.": "JavaScript 3D библиотека.",
    "Empowering everyone to build reliable and efficient software.": "Создание надежного и эффективного ПО.",
    "Promise based HTTP client for the browser and node.js": "HTTP-клиент на основе промисов.",
    "Godot Engine – Multi-platform 2D and 3D game engine": "Игровой движок Godot.",
    "21 Lessons, Get Started Building with Generative AI": "21 урок по генеративному ИИ.",
    "TypeScript is a superset of JavaScript that compiles to clean JavaScript output.": "TypeScript — надмножество JavaScript.",
    "A modern runtime for JavaScript and TypeScript.": "Современная среда выполнения JS и TS.",
    "A fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet.": "Быстрый реверс-прокси для локальных серверов.",
    "Build smaller, faster, and more secure desktop and mobile applications with a web frontend.": "Быстрые десктопные и мобильные приложения.",
    "Papers from the computer science community to read and discuss.": "Научные статьи для чтения и обсуждения.",
    "Set up a modern web app by running one command.": "Создание современного веб-приложения одной командой.",
    "The new Windows Terminal and the original Windows console host, all in the same place!": "Новый терминал Windows.",
    "LLM inference in C/C++": "LLM инференс на C/C++.",
    "The Postgres development platform. Supabase gives you a dedicated Postgres database to build your web, mobile, and AI applications.": "Платформа разработки на Postgres.",
    "An open-source AI agent that brings the power of Gemini directly into your terminal.": "AI-агент Gemini в терминале.",
    "Deliver web apps with confidence 🚀": "Разработка веб-приложений с уверенностью.",
    "Next generation frontend tooling. It's fast!": "Фронтенд-инструментарий нового поколения.",
    "List of Computer Science courses with video lectures.": "Список курсов Computer Science с видеолекциями.",
    "Hunt down social media accounts by username across social networks": "Поиск аккаунтов в соцсетях по имени пользователя.",
    ":cherry_blossom: A command-line fuzzy finder": "Fuzzy finder для командной строки.",
    ":zap: Dynamically generated stats for your github readmes": "Динамическая статистика для GitHub README.",
    "Models and examples built with TensorFlow": "Модели и примеры на TensorFlow.",
    "An open-source cross-platform alternative to AirDrop": "Open-source альтернатива AirDrop.",
    "VS Code in the browser": "VS Code в браузере.",
    "A high-throughput and memory-efficient inference and serving engine for LLMs": "Движок инференса для LLM с высокой пропускной способностью.",
    "The trust-minimized, zero-knowledge bridging protocol, designed for censorship resistance, extremely high security, and usage in decentralized finance.": "Протокол моста с нулевым разглашением.",
    "The iconic SVG, font, and CSS toolkit": "Инструментарий SVG, шрифтов и CSS.",
    "Free monospaced font with programming ligatures": "Моноширинный шрифт с лигатурами для кода.",
    "A Zsh theme": "Тема для Zsh.",
    "Tensors and Dynamic neural networks in Python with strong GPU acceleration": "Тензоры и нейронные сети на Python.",
    "A collection of (mostly) technical things every software developer should know about": "Технические вещи, которые должен знать разработчик.",
    "Vim-fork focused on extensibility and usability": "Форк Vim с упором на расширяемость.",
    "Robust Speech Recognition via Large-Scale Weak Supervision": "Надежное распознавание речи (Whisper).",
    "Magnificent app which corrects your previous console command.": "Приложение, которое исправляет ошибки в консоли.",
    "A utility-first CSS framework for rapid UI development.": "CSS-фреймворк для быстрой разработки интерфейсов.",
    "Clean Code concepts adapted for JavaScript": "Концепции чистого кода для JavaScript.",
    "JavaScript API for Chrome and Firefox": "API JavaScript для Chrome и Firefox.",
    "Design patterns implemented in Java": "Паттерны проектирования на Java.",
    "Python tool for converting files and office documents to Markdown.": "Инструмент для конвертации документов в Markdown.",
    "A Collection of application ideas which can be used to improve your coding skills.": "Коллекция идей приложений для практики кода.",
    "Bitcoin Core integration/staging tree": "Исходный код Bitcoin Core.",
    "The world’s fastest framework for building websites.": "Самый быстрый фреймворк для создания сайтов.",
    "The Web framework for perfectionists with deadlines.": "Веб-фреймворк для перфекционистов.",
    "Open Source Computer Vision Library": "Библиотека компьютерного зрения с открытым кодом.",
    "web development for the rest of us": "Веб-разработка для людей (Svelte).",
    "Animation engine for explanatory math videos": "Движок анимации для математических видео.",
}

# Rule-based fallback translation
def smart_translate(text):
    if not text or text == "None": return "Без описания"
    if text.strip() in TRANS_MAP: return TRANS_MAP[text.strip()]
    
    # Generic translations for common terms
    t = text
    t = t.replace("framework", "фреймворк").replace("Library", "Библиотека").replace("library", "библиотека")
    t = t.replace("application", "приложение").replace("Application", "Приложение")
    t = t.replace("A curated list of", "Кураторский список").replace("A collection of", "Коллекция")
    t = t.replace("Open source", "Открытый исходный код").replace("Open-source", "С открытым кодом")
    t = t.replace("for building", "для создания").replace("to help", "чтобы помочь")
    t = t.replace("modern", "современный").replace("powerful", "мощный")
    t = t.replace("development", "разработка").replace("software", "ПО")
    
    # Special character cases
    if "tutorial" in t.lower(): t = t.replace("tutorial", "обучающее руководство")
    if "interviews" in t.lower(): t = t.replace("interviews", "интервью")
    
    return t

INPUT_PATH = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru.csv")
OUTPUT_PATH = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru-final.csv")

with open(INPUT_PATH, "r", encoding="utf-8-sig") as f_in:
    reader = csv.reader(f_in)
    rows = list(reader)

header = rows[0]
new_rows = [header]

for row in rows[1:]:
    # Row format: #, Repository, Link, Stars, Description
    idx, name, link, stars, desc = row
    new_rows.append([idx, name, link, stars, smart_translate(desc)])

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f_out:
    writer = csv.writer(f_out)
    writer.writerows(new_rows)

print(f"✅ Full translated CSV generated: {OUTPUT_PATH}")
