---
tags: [nexus-vault, security, PGP, GPG, encryption, identity, private-key]
category: Security / Cryptographic Identity & Encryption (OpenPGP)
language: C / C++ / Python (GPGME)
github: https://github.com/gpg/gnupg (Official GnuPG)
---

# GPG — GNU Privacy Guard (The OpenPGP Standard)

## Описание
**GnuPG (GPG)** — это свободная реализация стандарта **OpenPGP**. Это самый надежный в мире инструмент для **шифрования и цифровой подписи** сообщений, файлов и кода. GPG позволяет вам создать пару "Публичный ключ + Приватный ключ" (Asymmetric Cryptography), чтобы обмениваться данными так, что их не сможет прочитать никто, кроме получателя. Это основа безопасности для разработчиков, активистов и системных администраторов.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | libgcrypt (Cryptographic library) |
| Standards | RFC 4880 (OpenPGP), RFC 6637 (ECC support) |
| Algorithms | RSA, ElGamal, DSA, AES, Camellia, Ed25519 (Modern) |
| Key Storage | Keyring (Local / Smartcards / YubiKey) |
| Interface | CLI (`gpg`), GPGME (API for Python/Go) |

## Почему это Killer-App
1. **Secret Identity**— позволяет вам подписывать свои коммиты в Git, гарантируя всем 1400+ репозиториям, что код прислали именно вы.
2. **Asymmetric Security**— можно публиковать свой "Публичный ключ" открыто, чтобы любой мог прислать вам зашифрованный "Секрет".
3. **Web of Trust (WoT)**— модель децентрализованного доверия, где пользователи подписывают ключи друг друга, доказывая их подлинность.
4. **Hardware Keys**— поддержка аппаратных токенов (напр. YubiKey), что делает кражу ключа физически невозможной.
5. **No Master Key**— в отличие от корпоративных сертификатов, здесь нет "главного" органа, который может отозвать ваш ключ.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Непроницаемая Агентская Связь (Hardened Agent Identity). Все команды от NEXUS Orchestrator к агентам должны подписываться GPG-ключом.
- **Интеграция:** Модуль NEXUS Keyring — управление GPG-ключами для подписи результатов OSINT-разведки.
- [[ANYTHING-LLM]] -> [[GPG]] зашифровка отчетов Obsidian.

## Пример использования (CLI)
```bash
# 1. Генерация ключа (следуйте инструкциям)
gpg --full-generate-key

# 2. Зашифровка файла для получателя 'nexus_admin'
gpg --encrypt --recipient nexus_admin secret_report.txt

# 3. Подпись файла (доказательство авторства)
gpg --sign report.pdf
```

## Связанные Репозитории
- [[BOTAN]] / [[CRYPTOGRAPHY]] — библиотеки для кода
- [[CRYFS]] — если нужно шифровать целые папки
- [[ETHICAL-HACKING-NOTES]] — как ломают (через перехват приватных ключей)
- [[GITHUB-PR-WORKFLOW]] — подпись коммитов в PR
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен поиск
- [[APPLICATIONINSPECTOR]] — анализ безопасности кода GPG
- [[CLEAN-CODE-JAVASCRIPT]] — чистота кода
- [[ASTRO]] / [[ELECTRON]] — создание интерфейса для GPG
- [[FFMPEG]] — если нужно зашифровать видео
- [[FACE-RECOGNITION]] — если лица связаны с цифровой личностью PGP
- [[FASTCHAT]] / [[FASTAPI]] — если шифрование управляет диалогом
- [[ENG-INTERVIEW]] — уметь объяснить структуру криптографии
- [[ESP32]] — если микроконтроллеры используют PGP (сложно, но возможно)
- [[FAIRY-DOCKER]] — если нужно упаковать GPG в контейнер
- [[GIN]] — скоростной веб-шлюз для PGP сервисов
- [[GPT-API]] / [[XLM]] — если нужно понимать зашифрованные тексты
- [[GRAFANA]] — мониторинг использования ключей
- [[GORELEASER]] — подпись бинарников GPG-ключом
