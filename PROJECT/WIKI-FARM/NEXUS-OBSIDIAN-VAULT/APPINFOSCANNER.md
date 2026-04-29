---
tags: [nexus-vault, security, mobile, android, ios, scanner]
category: Security / Mobile Apps Audit
language: Python / Java / Kotlin / Swift
github: https://github.com/Charles0429/AppInfoScanner
---

# APPINFOSCANNER — Mobile Application Vulnerability Scanner

## Описание
**AppInfoScanner** — это комплексный инструмент на **Python** для автоматического анализа мобильных приложений (**Android APK, iOS IPA**). Он сканирует исходный код и ресурсы приложений на предмет утечки конфиденциальной информации, API-ключей, уязвимых путей (URL) и "захардкоренных" данных.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.7+ |
| Backend | Dex2jar, JD-GUI (Android), App-inspect (iOS) |
| Targets | APK (Android), IPA (iOS), APP (macOS), EXE (Windows) |
| Reporting | JSON / HTML / Excel |

## Ключевые Возможности
1. **Creds Extraction** — автоматический поиск паролей, AWS-ключей, Firebase-секретов.
2. **Reverse Engineering** — декомпиляция APK/IPA для поиска уязвимых алгоритмов.
3. **URL Discovery** — вытягивание всех эндпоинтов (API URLs), зашитых в коде.
4. **Dangerous Permissions** — аудит разрешений (камера, контакты, микрофон).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автоматизированный аудит безопасности кода (Mobile focus).
- **Интеграция:** Модуль NEXUS Recon может использовать AppInfoScanner для проверки "доверенности" скачиваемых приложений.
- **Ключевое:** Работает с декомпилированным кодом (Bytecode), а не только с манифестом.

## Пример запуска в Linux/Windows
```bash
# Рекурсивное сканирование папки с APK файлами
python AppInfoScanner.py -p /path/to/apk_files/

# Фокус на поиске конкретных ключевых слов (напр. "nexus")
python AppInfoScanner.py -p my_app.apk --keyword "nexus"
```

## Связанные Репозитории
- [[APPLICATIONINSPECTOR]] — анализ исходного кода от Microsoft
- [[ANDROID-PIN-BRUTEFORCE]] — брутфорс PIN-кодов (Offense)
- [[CHATSECURE-IOS]] — защищенный мессенджер для iOS
- [[APPWRITE]] — мобильный бэкенд
