import csv
import re

# English to Russian mapping for GitHub repo descriptions
# Generated using NEXUS Cognitive Engine v5.0
translations = {
    "Master programming by recreating your favorite technologies from scratch.": "Освойте программирование, воссоздавая любимые технологии с нуля.",
    "😎 Awesome lists about all kinds of interesting topics": "😎 Потрясающие списки на самые разные интересные темы.",
    "freeCodeCamp.org's open-source codebase and curriculum. Learn math, programming, and computer science for free.": "Open-source база и учебная программа freeCodeCamp.org. Изучайте математику и программирование бесплатно.",
    "A collective list of free APIs": "Коллективный список бесплатных API.",
    ":books: Freely available programming books": ":books: Бесплатные книги по программированию.",
    "Interactive roadmaps, guides and other educational content to help developers grow in their careers.": "Интерактивные дорожные карты и учебный контент для развития карьеры разработчика.",
    "Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞": "Ваш персональный AI-ассистент. Любая ОС. Любая платформа. В стиле лобстера. 🦞",
    "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.": "Узнайте, как проектировать масштабируемые системы. Подготовка к системному интервью.",
    "A complete computer science study plan to become a software engineer.": "Полный план обучения компьютерным наукам для становления инженером.",
    "An opinionated list of Python frameworks, libraries, tools, and resources": "Субъективный список Python-фреймворков, библиотек и инструментов.",
    "A list of Free Software network services and web applications which can be hosted on your own servers": "Список сетей и веб-приложений для хостинга на собственных серверах.",
    "Repo for counting stars and contributing. Press F to pay respect to glorious developers.": "Репо для подсчета звезд и вкладов. Нажмите F, чтобы выразить уважение разработчикам.",
    "Curated list of project-based tutorials": "Кураторский список туториалов на основе проектов.",
    "The library for web and native user interfaces.": "Библиотека для веб-интерфейсов и нативных интерфейсов.",
    "Linux kernel source tree": "Исходный код ядра Linux.",
    "All Algorithms implemented in Python": "Все алгоритмы, реализованные на Python.",
    "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and more.": "Коллекция списков, мануалов, читшитов и хаков.",
    "This is the repo for Vue 2. For Vue 3, go to https://github.com/vuejs/core": "Репозиторий Vue 2. Для Vue 3 перейдите по ссылке.",
    "🎓 Path to a free self-taught education in Computer Science!": "🎓 Путь к бесплатному самообразованию в Computer Science!",
    "📝 Algorithms and data structures implemented in JavaScript with explanations and links to further readings": "📝 Алгоритмы и структуры данных на JavaScript.",
    "An Open Source Machine Learning Framework for Everyone": "Фреймворк машинного обучения с открытым исходным кодом для всех.",
    "🙃   A delightful community-driven (with 2,400+ contributors) framework for managing your zsh configuration. Includes 300+ optional plugins (rails, git, macOS, hub, docker, homebrew, node, php, python, etc), 140+ themes to spice up your morning, and an auto-update tool that makes it easy to keep up with the latest updates from the community.": "Фреймворк для управления конфигурацией zsh с 300+ плагинами и 140+ темами.",
    "A book series (2 published editions) on the JS language.": "Серия книг по языку JavaScript.",
    "技术面试必备基础知识、Leetcode、计算机操作系统、计算机网络、系统设计": "Базовые знания для тех. интервью, Leetcode, ОС, сети, системный дизайн.",
    "Visual Studio Code": "Visual Studio Code.",
    "AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters.": "AutoGPT — видение доступного ИИ для всех.",
    "Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.": "Платформа автоматизации воркфлоу с нативным ИИ.",
    "Python - 100天从新手到大师": "Python - от новичка до мастера за 100 дней.",
    "Flutter makes it easy and fast to build beautiful apps for mobile and beyond": "Flutter позволяет быстро создавать красивые мобильные приложения.",
    "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.": "Самый популярный фреймворк для адаптивной верстки.",
    "A collection of useful .gitignore templates": "Коллекция полезных шаблонов .gitignore.",
    "Open-source Windows and Office activator featuring HWID, Ohook, TSforge, and Online KMS activation methods, along with advanced troubleshooting.": "Open-source активатор Windows и Office.",
    "A curated list of awesome Go frameworks, libraries and software": "Кураторский список фреймворков и библиотек для Go.",
    "Get up and running with Kimi-K2.5, GLM-5, MiniMax, DeepSeek, gpt-oss, Qwen, Gemma and other models.": "Запуск моделей Kimi-K2.5, GLM-5, DeepSeek, gpt-oss и др.",
    "The repo is finally unlocked. enjoy the party! The fastest repo in history to surpass 100K stars ⭐. Join Discord: https://discord.gg/5TUQKqFWd Built in Rust using oh-my-codex.": "Репо разблокирован! Самый быстрый репо, набравший 100K звезд. Написан на Rust.",
    "Stable Diffusion web UI": "Веб-интерфейс для Stable Diffusion.",
    "Master the command line, in one page": "Освоение командной строки на одной странице.",
    "🤗 Transformers: the model-definition framework for state-of-the-art machine learning models in text, vision, audio, and multimodal models, for both inference and training.": "🤗 Transformers: фреймворк для современных моделей машинного обучения.",
    "f.k.a. Awesome ChatGPT Prompts. Share, discover, and collect prompts from the community. Free and open source — self-host for your organization with complete privacy.": "Делитесь и находите промпты для ChatGPT.",
    "DigitalPlat FreeDomain: Free Domain For Everyone": "Бесплатные домены для всех.",
    "A feature-rich command-line audio/video downloader": "Полнофункциональный загрузчик аудио/видео.",
    "Java 面试 & 后端通用面试指南，覆盖计算机基础、数据库、分布式、高并发、系统设计与 AI 应用开发": "Гайд по Java-интервью: базы данных, системы, ИИ.",
    ":octocat: 分享 GitHub 上有趣、入门级的开源项目。Share interesting, entry-level open source projects on GitHub.": "Интересные open-source проекты начального уровня на GitHub.",
    "JavaScript Style Guide": "Гайд по стилю написания JavaScript.",
    "Langflow is a powerful tool for building and deploying AI-powered agents and workflows.": "Инструмент для создания и деплоя ИИ-агентов.",
    "Command-line program to download videos from YouTube.com and other video sites": "Программа для загрузки видео с YouTube и других сайтов.",
    "The React Framework": "Фреймворк React.",
    "Curated coding interview preparation materials for busy software engineers": "Материалы для подготовки к интервью.",
    "Display and control your Android device": "Отображение и управление вашим Android устройством.",
    "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.": "Система оптимизации производительности агентов.",
    "The open source coding agent.": "Агент для написания кода с открытым исходным кодом.",
    "Production-ready platform for agentic workflow development.": "Платформа для разработки агентных воркфлоу.",
    "An agentic skills framework & software development methodology that works.": "Фреймворк агентных скиллов и методология разработки.",
    "The Go programming language": "Язык программирования Go.",
    "Crack LeetCode, not only how, but also why.": "Взлом LeetCode: не только как, но и почему.",
    "The agent engineering platform": "Платформа проектирования агентов.",
    "Microsoft PowerToys is a collection of utilities that supercharge productivity and customization on Windows": "Утилиты для повышения производительности в Windows.",
    "User-friendly AI Interface (Supports Ollama, OpenAI API, ...)": "Пользовательский интерфейс ИИ (Ollama, OpenAI API).",
    "Coding articles to level up your development skills": "Статьи по программированию для повышения навыков.",
    "A framework for building native applications using React": "Фреймворк для нативных приложений на React.",
    "《Hello 算法》：动画图解、一键运行的数据结构与算法教程。支持简中、繁中、English、日本語，提供 Python, Java, C++, C, C#, JS, Go, Swift, Rust, Ruby, Kotlin, TS, Dart 等代码实现": "Анимированный гид по структурам данных и алгоритмам.",
    "Production-Grade Container Scheduling and Management": "Управление контейнерами промышленного уровня.",
    ":electron: Build cross-platform desktop apps with JavaScript, HTML, and CSS": ":electron: Десктоп-приложения на JS, HTML и CSS.",
    "A list of SaaS, PaaS and IaaS offerings that have free tiers of interest to devops and infradev": "Список SaaS/PaaS с бесплатными тарифами.",
    "Virtual whiteboard for sketching hand-drawn like diagrams": "Виртуальная доска для рисования диаграмм.",
    "Node.js JavaScript runtime ✨🐢🚀✨": "Среда выполнения Node.js.",
    "免费的计算机编程类中文书籍，欢迎投稿": "Бесплатные книги по программированию на китайском.",
    "Collection of publicly available IPTV channels from all over the world": "Коллекция публичных IPTV каналов со всего мира.",
    "Bring data to life with SVG, Canvas and HTML. :bar_chart::chart_with_upwards_trend::tada:": "Визуализация данных с помощью SVG, Canvas и HTML.",
    "JavaScript 3D Library.": "JavaScript 3D библиотека.",
    "Empowering everyone to build reliable and efficient software.": "Создание надежного и эффективного ПО.",
    "A set of beautifully-designed, accessible components and a code distribution platform. Works with your favorite frameworks. Open Source. Open Code.": "Красивые и доступные компоненты интерфейса.",
    "An open-source remote desktop application designed for self-hosting, as an alternative to TeamViewer.": "Open-source приложение для удаленного рабочего стола.",
    "Public repository for Agent Skills": "Публичный репозиторий скиллов агентов.",
    "A collection of various awesome lists for hackers, pentesters and security researchers": "Списки для хакеров и исследователей безопасности.",
    "Promise based HTTP client for the browser and node.js": "HTTP-клиент на основе промисов.",
    "Godot Engine – Multi-platform 2D and 3D game engine": "Игровой движок Godot.",
    "21 Lessons, Get Started Building with Generative AI": "21 урок по генеративному ИИ.",
    "Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands.": "Агентный инструмент в терминале для работы в кодом.",
    "TypeScript is a superset of JavaScript that compiles to clean JavaScript output.": "TypeScript — надмножество JavaScript.",
    "The most powerful and modular diffusion model GUI, api and backend with a graph/nodes interface.": "Мощный графический интерфейс для диффузионных моделей.",
    "A modern GUI client based on Tauri, designed to run in Windows, macOS and Linux for tailored proxy experience": "Современный GUI клиент на Tauri для прокси.",
    ":cn: GitHub中文排行榜，各语言分设「软件 | 资料」榜单，精准定位中文好项目。各取所需，高效学习。": "Китайский чарт репозиториев GitHub.",
    "A modern runtime for JavaScript and TypeScript.": "Современная среда выполнения JS и TS.",
    "A fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet.": "Быстрый реверс-прокси для локальных серверов.",
    ":white_check_mark:  The Node.js best practices list (July 2024)": "Бести по Node.js (Июль 2024).",
    "Build smaller, faster, and more secure desktop and mobile applications with a web frontend.": "Создание быстрых десктопных и мобильных приложений.",
    "Papers from the computer science community to read and discuss.": "Научные статьи для чтения и обсуждения.",
    "Collection of awesome LLM apps with AI Agents and RAG using OpenAI, Anthropic, Gemini and opensource models.": "Коллекция LLM-приложений с агентами и RAG.",
    "🔥 The Web Data API for AI - Power AI agents with clean web data": "🔥 API веб-данных для ИИ.",
    "Set up a modern web app by running one command.": "Создание современного веб-приложения одной командой.",
    "The new Windows Terminal and the original Windows console host, all in the same place!": "Новый терминал Windows.",
    " This project is dedicated to collecting high-quality macOS software and organizing them systematically by different categories for easy search and use.": "Качественное ПО для macOS.",
    "LLM inference in C/C++": "LLM инференс на C/C++.",
    "A GUI client for Windows, Linux and macOS, support Xray and sing-box and others": "GUI клиент для Windows, Linux и macOS.",
    "The Postgres development platform. Supabase gives you a dedicated Postgres database to build your web, mobile, and AI applications.": "Платформа разработки на Postgres.",
    "An open-source AI agent that brings the power of Gemini directly into your terminal.": "AI-агент Gemini в терминале.",
    "Deliver web apps with confidence 🚀": "Разработка веб-приложений с уверенностью."
}

def translate(text):
    return translations.get(text.strip(), text.strip())

with open("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI/github-top-stars.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Parse the table using regex
pattern = r"\| \[(.*?)\]\((.*?)\) \| (.*?) \| (.*?) \|"
matches = re.findall(pattern, md_content)

with open("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI/github-top-stars-ru.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Репозиторий", "Ссылка", "Звезды", "Описание (Русский)"])
    for match in matches:
        name, url, stars, desc = match
        writer.writerow([name, url, stars, translate(desc)])

print(f"Successfully processed {len(matches)} repositories.")
