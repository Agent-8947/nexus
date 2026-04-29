---
tags: [nexus-vault, security, osint, pentest, red-team, blue-team, ics, iot, ctf, chinese]
category: Security / Comprehensive Knowledge Framework
language: Markdown, Bash, Python, PowerShell
github: https://github.com/ffffffff0x/1earn
---

# 1EARN — Универсальная База Знаний по Безопасности

## Описание
Колоссальная база знаний по информационной безопасности, поддерживаемая командой `ffffffff0x`. Охватывает весь спектр: OSINT, Red Team (Web, OS, Protocol, Cloud), Blue Team (форензика, реагирование, усиление), ICS/SCADA безопасность, IOT, Crypto, CTF, реверс-инжиниринг. Структурирована как практическая энциклопедия с cheat sheet, команд и реальными кейсами. Написана на китайском — уникальный источник с незападной перспективой на безопасность.

## Основные Разделы
1. **RedTeam** — Exploitation (веб, ОС, протоколы, облако), Post-Exploitation, Wireless, Social Engineering
2. **BlueTeam** — Форензика (диск, память, USB), мониторинг, харденинг, incident response
3. **OSINT / Recon** — пространственное картирование, сканирование портов, перечисление, fingerprinting
4. **ICS Security** — атаки на PLC, S7comm, промышленные протоколы
5. **IOT** — анализ прошивок, аппаратная безопасность, HID
6. **Crypto** — все алгоритмы шифрования и атаки
7. **CTF** — инструменты и writeup архив

## Почему это Killer-App
- **Незападная перспектива** — уникальные техники, специфичные для азиатского сегмента инфраструктуры.
- **ICS/SCADA глубина** — редкий источник по атакам на промышленные системы управления.
- **Methodology-first** — не просто команды, а полные Attack Chains.
- **Dual Coverage** — Red Team И Blue Team в одном репо = полный defense/offense цикл.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Master Reference для Security Agent — все cheat sheet в одном месте для RAG-поиска.
- **Интеграция:** NEXUS Security Lab Agent использует этот vault как knowledge base для генерации Playbook.
- **Ключевое:** ICS раздел критичен для NEXUS Industrial Monitoring Agents (`DNA_08_Engine_Config` → mission=iot_recon).

## Топ-3 примера

```bash
# OSINT: пространственное картирование
shodan search "port:80 country:CN org:Alibaba"

# Pentest: перечисление SMB
nmap --script smb-enum-shares,smb-enum-users -p 445 192.168.1.0/24

# Post-Exploit: поиск повышения привилегий Linux
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | bash
```

## Связанные Репозитории
- [[ETHICAL-HACKING-NOTES]] — западный аналог — методология пентеста
- [[AWESOME-HACKING]] — кураторский список инструментов
- [[SPIDERFOOT]] — OSINT автоматизация
- [[RECONFTW]] — автоматический Red Team разведчик
- [[CHIPSEC]] — безопасность на уровне железа
