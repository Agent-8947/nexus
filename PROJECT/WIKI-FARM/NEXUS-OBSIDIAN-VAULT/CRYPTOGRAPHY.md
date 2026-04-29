---
tags: [nexus-vault, security, python, cryptography, openssl, hazard-layered]
category: Security / Cryptography Toolkit (Standard)
language: Python / C
github: https://github.com/pyca/cryptography
---

# CRYPTOGRAPHY — The Industry Standard Python Library (PyCA)

## Описание
**Cryptography** (от PyCA) — это самая надежная и широко используемая библиотека в экосистеме **Python** для реализации любых криптографических операций. Она разработана с принципом "безопасность по умолчанию": в ней сложно ошибиться и случайно использовать плохой алгоритм или слабый ключ. На ней построены тысячи проектов, включая Django, Twisted, Ansible и другие.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | C / Rust (backend) / OpenSSL |
| Interface | Python 3.7+ |
| Layers | Fernet (High-level) / Recipes (Mid) / Hazmat (Low-level) |
| Performance | Сверхбыстрая работа за счет C-биндингов |

## Почему это Killer-App
1. **Fernet (High-level)**— единственный способ зашифровать строку "в 3 строчки кода", который гарантированно безопасен (AES-CBC + HMAC-SHA256).
2. **Hazmat (Hazardous Materials)**— низкоуровневые элементы (Elliptic Curves, Padding, Block Modes) для экспертов, выделенные в отдельный модуль для предотвращения случайных ошибок.
3. **Rust Backend**— часть ядра переписана на Rust для защиты от атак на память.
4. **X.509 Support**— самая мощная в Python библиотека для генерации и проверки SSL/TLS сертификатов.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Надежное Шифрование Приложения (App-level Encryption). Использование Fernet для шифрования всех `memory.json` файлов ваших агентов.
- **Интеграция:** Модуль NEXUS Key Manager — генерация, хранение и ротация ключей шифрования.
- **Ключевое:** Поддержка всех современных протоколов (Ed25519, X25519, Poly1305).

## Пример: Шифрование данных (Fernet)
```python
from cryptography.fernet import Fernet

# 1. Генерация ключа (сохраните его!)
key = Fernet.generate_key()
f = Fernet(key)

# 2. Шифрование "секрета"
token = f.encrypt(b"NEXUS Confidential Intelligence")

# 3. Расшифровка
decrypted = f.decrypt(token)
print(decrypted.decode())
```

## Связанные Репозитории
- [[BOTAN]] — альтернатива на С++
- [[CRYFS]] — шифрованная файловая система
- [[BORG]] — пример использования криптографии в архивах
- [[CERTIFICATES]] — управление SSL сертификатами
- [[AEGIS]] — аутентификация пользователя
