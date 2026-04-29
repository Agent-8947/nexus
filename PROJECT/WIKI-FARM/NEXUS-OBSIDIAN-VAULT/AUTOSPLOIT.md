---
tags: [nexus-vault, security, osint, exploit, metasploit, shodan]
category: Security / Offensive / OSINT
language: Python
github: https://github.com/NullArray/AutoSploit
---

# AUTOSPLOIT — Automated Mass Exploitation

## Описание
Автоматизирует **сбор целей** через Shodan/Censys/Zoomeye и **эксплуатацию** через модули Metasploit Framework. Полная цепочка: поиск уязвимых хостов → подбор эксплоита → получение reverse shell.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 2/3 |
| OSINT Engine | Shodan API, Censys, Zoomeye |
| Exploit Engine | Metasploit RPC API |
| Payloads | Meterpreter, reverse TCP/HTTPS |
| Target Discovery | Автоматический по CVE/сервису |

## Механика Работы
```
[1] Target Discovery
    Shodan Query: "apache 2.4.49" → список IP
    
[2] Exploit Selection
    CVE → Metasploit module mapping
    
[3] Automated Exploitation
    For each target:
        msf.execute(exploit, target_ip, payload)
        
[4] Post-Exploitation
    Meterpreter session → loot / pivot
```

## Ключевые Фичи
- **Shodan Integration:** `shodan search "port:445 os:Windows"` → автоматический список целей
- **Censys/Zoomeye:** альтернативные поисковые движки
- **Metasploit RPC:** программный контроль MSF через API
- **Custom Queries:** свои NSE/Shodan запросы для таргетинга

## Архитектурная Ценность для NEXUS
- **Паттерн:** Полный pipeline "Discover → Exploit → Report" — шаблон для любого автономного агента
- **Интеграция:** Shodan API + автоматический отбор целей = модель для NEXUS OSINT-агента
- **Риск:** Очень высокий. Только для авторизованного пентеста / Red Team

## Связанные Репозитории
- [[AWESOME-SHODAN-QUERIES]] — коллекция Shodan-запросов
- [[ATTACKSURFACEANALYZER]] — анализ поверхности атаки
- [[CAMERADAR]] — RTSP-сканирование
- [[CHAOS-ROOTKIT]] — rootkit x64
- [[CHEATSHEET-GOD]] — OSCP шпаргалки
