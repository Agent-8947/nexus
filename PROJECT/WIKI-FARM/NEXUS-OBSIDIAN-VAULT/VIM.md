---
tags: [nexus-vault, tools, terminal, vim, editor, speed, efficiency, keyboard-only, ssh, linux]
category: Tools / High-efficiency Modal Text Editor (The Master's Tool)
language: C (Core) / VimScript / Lua (Neovim)
github: https://github.com/vim/vim (Classic) / https://github.com/neovim/neovim (Modern fork)
---

# VIM — Vi IMproved: The Ubiquitous Modal Text Editor (Speed & Focus)

## Описание
**Vim** (и его современный наследник **Neovim**) — это легендарный текстовый редактор с открытым исходным кодом, предназначенный для невероятно быстрой и эффективной работы с кодом и текстами прямо в терминале. В отличие от обычных редакторов (напр. [[VSCODE]]), Vim является **модальным**: у него есть специальные режимы для ввода текста, его выделения и, самое важное, — для быстрой навигации и манипуляции им с помощью одних только горячих клавиш. Мастерство Vim позволяет системному инженеру NEXUS исправлять конфиги на удаленных серверах [[UBUNTU]] через SSH со скоростью мысли, не прикасаясь к мышке.

## Технический Стек (The Editor Infrastructure)
| Компонент | Технология |
|-----------|------------|
| Core Engine | C / Lua (Plugin engine in Neovim) |
| Architecture | Modal (Normal, Insert, Visual, Command modes) |
| Performance | Instant startup, Runs on any terminal (Local/SSH) |
| Keybindings | H-J-K-L (Navigation), d-w (Delete word), c-i-w (Change inside word) |
| Package Manager | Lazy.nvim, Packer, Vundle (Modern plugin ecosystem) |
| Standards | LSP (Language Server Protocol - IDE features for Vim) |

## Почему это Killer-App
1. **Unrivaled Efficiency Mastery**— Вы больше не тратите время на перенос руки к мышке. Каждое действие — это короткая "фраза" на клавиатуре: `ci"` (изменить текст в кавычках). Вы работаете в потоке (Flow State).
2. **Infinite Portability Power**— Vim предустановлен практически на каждом Linux-сервере в мире. Куда бы вас ни забросила OSINT-разведка (SSH), вы всегда "дома".
3. **Low Resource Footprint Mastery Mastery**— Vim запускается мгновенно даже на слабейшем [[ESP32]] (через busybox) или перегруженном сервере. Вы никогда не ждете, пока "загрузится IDE".
4. **Extreme Automation Power**— Встроенные макросы (клавиша `q`) позволяют записать сложное действие один раз и повторить его 10 000 раз для всего файла досье Wiki за секунду.
5. **Aesthetic Focus Power**— Никаких отвлекающих меню, кнопок и панелей. Только вы, ваш код и ваш терминал в стиле "хакерской классики".

## Архитектурная Ценность для NEXUS
- **Паттерн:** Мастер-Инструмент Терминала (The Master Terminal Tool). Основное "оружие" для правки конфигов, скриптов и досье прямо на удаленных базах.
- **Интеграция:** Модуль NEXUS Editor — использование Neovim с настроенными плагинами для оцифровки и ручной коррекции 1400+ репозиториев.
- [[SLOW MOUSE EDIT]] -> [[VIM MOTIONS]] -> [[SPEED OF THOUGHT]] мастерство.

## Пример команд (Vim / The Basics)
```vim
# 1. Навигация (Normal Mode)
# j (вниз), k (вверх), h (влево), l (вправо)

# 2. Магия редактирования
# ci"  - удалить всё внутри кавычек и начать писать заново
# ddp  - поменять местами две строки кода
# ggVG - выделить весь текст файла (Go Go Visual Global)

# 3. Сохранение и выход
# :w  - Сохранить (Write)
# :q! - Выйти без сохранения (Quit!)
# :wq - Сохранить и выйти (Классика)
```

## Связанные Репозитории (The Editor Grid)
- [[VSCODE]] — (у него есть плагин "Vim Mode", чтобы совместить миры)
- [[UBUNTU]] / [[ZSH]] — среда, где Vim чувствует себя как король
- [[PYTHON]] — (лучшие плагины для Vim написаны на Python / Lua)
- [[GIT]] — (Vim — стандартный редактор для Git-коммитов)
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в редакторе нужен ИИ-поиск (через Copilot.vim)
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian (написан на JS, но заметки пишутся в Vim)
- [[CRAWL4AI]] — сборщик данных (топливо для текстов в Vim)
- [[ETHICAL-HACKING-NOTES]] — как работать в терминале при взломах
- [[ALLUXIO]] — (неприменимо напрямую)
- [[ASTRO]] / [[NEXTJS]] — современные фронтенды (код пишется в Neovim)
- [[ELECTRON]] — (неприменимо напрямую)
- [[FFMPEG]] — (неприменимо напрямую)
- [[FACE-RECOGNITION]] — (неприменимо напрямую)
- [[FASTCHAT]] / [[FASTAPI]] — API управления фронтендом
- [[ESP32]] — (неприменимо напрямую)
- [[FAIRY-DOCKER]] — легкие контейнеры для инструментов
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — защита секретных файлов, которые вы правите в Vim
- [[HA-PROXY]] — нагрузка на кластер
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — перевод названий сервисов (i18n)
- [[GBDT]] — (неприменимо напрямую)
- [[HASHCAT]] — (неприменимо напрямую)
- [[HELM]] / [[KUBERNETES]] — запуск нод в кластере (Vim для правки YAML)
- [[HTOP]] — мониторинг ресурсов CPU/RAM
- [[HARBOR]] — реестр образов для инструментов
- [[HEDGEDOC]] — документация проекта
- [[INTERPRETABLE-ML]] — объяснение работы систем на базе UI
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — (неприменимо напрямую)
- [[IMAGE-PROCESSING]] — (неприменимо напрямую)
- [[IMAGES-PYTHON]] — (неприменимо напрямую)
- [[IMMLIB]] — (низкоуровневая отладка бинарников)
- [[INFRASTRUCTURE]] — как всё связано (Мастер-чертеж)
- [[IP-ADDR]] — чистая работа с IP (Field type "string")
- [[IP-RECON]] — разведка IP
- [[JAVA]] — (IDE focus, но Vim-LSP работает и с Java)
- [[JAVASCRIPT-ALGORITHMS]] — ИИ на JS (в браузере)
- [[JENKINS]] — отладка пайплайнов деплоя
- [[JINJA2]] — (неприменимо напрямую)
- [[JOB-INTEL]] — OSINT бот по вакансиям DevOps-инженеров
- [[JUPYTER]] — лаборатория анализа (Vim-плагины для ноутбуков)
- [[KIBANA]] — анализ логов всей сети
- [[KIND]] — запуск локального кластера
- [[KUBERNETES]] — фундамент (повторно)
- [[LANGCHAIN]] — (агенты, умеющие писать код в стиле Vim)
- [[LEARN-LINUX]] — ОС для запуска Вики-фермы (главный фокус)
- [[MASTER-PLAN]] — архитектурная основа
- [[ZEN]] — спокойствие админа (Редактор всегда под рукой)
- [[EMACS]] — главный исторический "противник" и партнер (другой путь скорости)
- [[NEOVIM]] — современный, быстрый, на Lua (рекомендуемый выбор)
- [[TMUX]] — (Terminal Multiplexer) лучший партнер для Vim
- [[ZSH]] / [[FISH]] — лучшие оболочки для работы с Vim
