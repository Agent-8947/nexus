import csv
import re
import sys
from pathlib import Path

# =====================================================================
# NEXUS CSV Translation Patcher v1.0
# Читает github-top-stars-full-ru-final.csv
# Заполняет пустые описания из TRANS_MAP
# Генерирует: github-top-stars-full-ru-PATCHED.csv
# =====================================================================

SOURCE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru-final.csv")
OUTPUT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru-PATCHED.csv")

# Полная карта переводов - собранная из translate_full_csv.py + наши новые добавку
TRANS_MAP = {
    "Master programming by recreating your favorite technologies from scratch.": "Освойте программирование, воссоздавая технологии с нуля.",
    "😎 Awesome lists about all kinds of interesting topics": "😎 Потрясающие списки на самые разные темы.",
    "A collective list of free APIs": "Коллективный список бесплатных API.",
    ":books: Freely available programming books": ":books: Бесплатные книги по программированию.",
    "Interactive roadmaps, guides and other educational content to help developers grow in their careers.": "Интерактивные дорожные карты для роста карьеры разработчика.",
    "Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞": "Персональный AI-ассистент. Любая ОС. В стиле лобстера. 🦞",
    "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.": "Дизайн масштабируемых систем. Подготовка к интервью.",
    "A complete computer science study plan to become a software engineer.": "Полный учебный план для становления инженером ПО.",
    "An opinionated list of Python frameworks, libraries, tools, and resources": "Субъективный список Python-фреймворков, библиотек и инструментов.",
    "A list of Free Software network services and web applications which can be hosted on your own servers": "Список ПО для хостинга на собственных серверах.",
    "Repo for counting stars and contributing. Press F to pay respect to glorious developers.": "Репо для подсчёта звёзд. Нажмите F, чтобы выразить уважение.",
    "Curated list of project-based tutorials": "Кураторский список проектных туториалов.",
    "The library for web and native user interfaces.": "Библиотека для веб- и нативных пользовательских интерфейсов.",
    "Linux kernel source tree": "Исходный код ядра Linux.",
    "All Algorithms implemented in Python": "Все алгоритмы, реализованные на Python.",
    "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and more.": "Коллекция вдохновляющих списков, мануалов, хаков и инструментов.",
    "This is the repo for Vue 2. For Vue 3, go to https://github.com/vuejs/core": "Репозиторий Vue 2. Для Vue 3 перейдите по ссылке.",
    "🎓 Path to a free self-taught education in Computer Science!": "🎓 Путь к бесплатному самообразованию в Computer Science!",
    "📝 Algorithms and data structures implemented in JavaScript with explanations and links to further readings": "📝 Алгоритмы и структуры данных на JavaScript с пояснениями.",
    "An Open Source Machine Learning Framework for Everyone": "Фреймворк машинного обучения с открытым кодом для всех.",
    "A book series (2 published editions) on the JS language.": "Серия книг по языку JavaScript (2 опубликованных издания).",
    "Visual Studio Code": "Редактор Visual Studio Code от Microsoft.",
    "AutoGPT is the vision of accessible AI for everyone, to use and to build on.": "Видение доступного ИИ для всех: использовать и строить на его основе.",
    "Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.": "Платформа автоматизации с нативным ИИ и 400+ интеграциями.",
    "Flutter makes it easy and fast to build beautiful apps for mobile and beyond": "Flutter: быстрое создание красивых приложений для мобильных и других платформ.",
    "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.": "Популярный HTML/CSS/JS фреймворк для адаптивной веб-разработки.",
    "A collection of useful .gitignore templates": "Коллекция полезных шаблонов .gitignore.",
    "Stable Diffusion web UI": "Веб-интерфейс для Stable Diffusion.",
    "Master the command line, in one page": "Освоение командной строки — всё на одной странице.",
    "A feature-rich command-line audio/video downloader": "Многофункциональная утилита для загрузки аудио/видео.",
    "JavaScript Style Guide": "Руководство по стилю JavaScript.",
    "Command-line program to download videos from YouTube.com and other video sites": "Программа для загрузки видео с YouTube и других сайтов.",
    "The React Framework": "Фреймворк React для продакшн-разработки.",
    "Curated coding interview preparation materials for busy software engineers": "Материалы для подготовки к техническому интервью для занятых инженеров.",
    "Display and control your Android device": "Управление Android-устройством с компьютера.",
    "The open source coding agent.": "Агент для написания кода с открытым исходным кодом.",
    "The Go programming language": "Язык программирования Go.",
    "Microsoft PowerToys is a collection of utilities that supercharge productivity and customization on Windows": "Коллекция утилит Microsoft для повышения продуктивности в Windows.",
    "Coding articles to level up your development skills": "Статьи по программированию для повышения навыков разработки.",
    "A framework for building native applications using React": "Фреймворк для создания нативных приложений на React.",
    "Production-Grade Container Scheduling and Management": "Управление и планирование контейнеров промышленного уровня.",
    ":electron: Build cross-platform desktop apps with JavaScript, HTML, and CSS": "Создание кросс-платформенных приложений на JS, HTML и CSS.",
    "Virtual whiteboard for sketching hand-drawn like diagrams": "Виртуальная доска для создания рукописных диаграмм.",
    "Node.js JavaScript runtime ✨🐢🚀✨": "Среда выполнения JavaScript Node.js.",
    "Collection of publicly available IPTV channels from all over the world": "Коллекция публичных IPTV-каналов со всего мира.",
    "JavaScript 3D Library.": "JavaScript-библиотека для 3D-графики.",
    "The lazier way to manage everything docker": "Ленивый способ управлять всем в Docker.",
    "Windows inside a Docker container.": "Windows внутри Docker-контейнера.",
    "Collection of learning resources for curious software engineers": "Коллекция учебных ресурсов для любознательных инженеров ПО.",
    "⭐️ Companies that don't have a broken hiring process": "⭐️ Компании с нормальным процессом найма без белых досок.",
    "100 Days of ML Coding": "100 дней программирования машинного обучения.",
    "Modern CSS framework based on Flexbox": "Современный CSS-фреймворк на основе Flexbox.",
    "Application Ideas Collection": "Коллекция идей для приложений по уровням сложности.",
    "Things Every Programmer Should Know": "То, что должен знать каждый программист.",
    "A curated list of awesome Go frameworks, libraries and software": "Кураторский список Go-фреймворков, библиотeks и инструментов.",
    "Tensor library for deep learning": "Библиотека тензоров для глубокого обучения (PyTorch).",
    "The open-source repo for docs.julialang.org": "Открытый репозиторий документации Julia.",
    "The JavaScript Framework": "JavaScript-фреймворк Angular от Google.",
    "A curated list of awesome C++ (or C) frameworks, libraries, resources, and shiny things.": "Кураторский список C++ фреймворков, библиотек и ресурсов.",
    "An awesome list that curates the best Docker tools, tutorials, articles and more!": "Список лучших Docker-инструментов, туториалов и статей.",
    "A curated list of awesome Java frameworks, libraries and software.": "Кураторский список Java-фреймворков, библиотек и инструментов.",
    "A curated list of awesome Rust code and resources.": "Кураторский список ресурсов и кода на Rust.",
    "A curated list of awesome Node.js packages and resources.": "Кураторский список Node.js-пакетов и ресурсов.",
    "Semantic Versioning 2.0.0": "Семантическое версионирование 2.0.0.",
    "The open-source platform for building and scaling AI applications.": "Открытая платформа для создания и масштабирования ИИ-приложений.",
    "Kubernetes (K8s) documentation": "Документация Kubernetes (K8s).",
    "A curated list of amazingly awesome Elixir and Erlang libraries, resources and shiny things.": "Кураторский список Elixir/Erlang библиотек и ресурсов.",
    "A curated list of awesome Swift programming language resources.": "Кураторский список ресурсов по Swift.",
}

# Fuzzy match helper
def normalize(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

# Build normalized lookup
norm_map = {normalize(k): v for k, v in TRANS_MAP.items()}

def translate(text):
    if not text:
        return text
    t = normalize(text)
    if t in norm_map:
        return norm_map[t]
    # Partial matching - if key starts with first 40 chars of original
    for k, v in norm_map.items():
        if t[:40] in k or k[:40] in t:
            return v
    return text  # Return original if no match found

def main():
    if not SOURCE.exists():
        print(f"❌ File not found: {SOURCE}")
        sys.exit(1)

    rows = []
    with open(SOURCE, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    header = rows[0]
    data = rows[1:]
    total = len(data)
    patched = 0
    still_english = 0

    result_rows = [header]
    for row in data:
        if len(row) >= 4 and row[3].strip():
            desc = row[3].strip()
            translated = translate(desc)
            if translated != desc:
                patched += 1
                row = list(row)
                row[3] = translated
            else:
                still_english += 1
        result_rows.append(row)

    with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result_rows)

    print(f"[NEXUS CSV Patcher] Done.")
    print(f"  Total rows:      {total}")
    print(f"  Patched:         {patched}")
    print(f"  Still English:   {still_english}")
    print(f"  Output:          {OUTPUT}")

if __name__ == "__main__":
    main()
