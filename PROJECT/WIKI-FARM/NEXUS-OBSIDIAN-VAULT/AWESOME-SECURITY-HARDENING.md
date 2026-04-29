---
tags: [nexus-vault, security, hardening, server-protection, infrastructure]
category: Security / Infrastructure Hardening
language: Markdown / Bash
github: https://github.com/tonybox/awesome-security-hardening
---

# AWESOME-SECURITY-HARDENING — Security Hardening Guide & Master List

## Описание
**Awesome Security Hardening** — это масштабный кураторский список лучших ресурсов, скриптов и руководств по **усилению защиты (hardening)** информационных систем. Это путь от "открытой всем ветрам" системы (default) до максимально защищенного периметра. Охватывает Linux, Windows, macOS, Cloud (AWS, GCP, Azure), Docker и Kubernetes.

## Разделы Hardening-а
1. **OS Level** — настройки ядра Linux (sysctl), конфиги SSH, PAM, SELinux/AppArmor.
2. **Cloud/Container** — CIS Benchmarks для Docker и K8s, безопасность образов.
3. **Web Standards** — конфигурация заголовков HTTP (HSTS, CSP), настройки Nginx/Apache.
4. **Network** — настройка фаерволов (iptables/nftables), VPN (Wireguard), IPS (Fail2Ban).
5. **Database** — защита MySQL, PostgreSQL, MongoDB от удаленного доступа.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Best Practices по Безопасности. Это стандарт, по которому должен быть настроен любой сервер NEXUS.
- **Интеграция:** Модуль NEXUS Hardener — автоматическое применение этих правил при разворачивании инфраструктуры.
- **Ключевое:** Использование готовых Ansible/Puppet/Terraform скриптов для массовой защиты хостов.

## Топ-3 Примера рекомендаций из Wiki
```bash
# 1. Отключение неиспользуемых протоколов в Linux (/etc/sysctl.conf)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# 2. Ограничение SSH по конкретным пользователям (/etc/ssh/sshd_config)
AllowUsers nexus_admin_only
PermitRootLogin no

# 3. Настройка фаервола (UFW) - разрешаем только NEXUS трафик
ufw default deny incoming
ufw limit ssh/tcp
ufw allow 80,443/tcp
ufw enable
```

## Связанные Репозитории
- [[ATTACKSURFACEANALYZER]] — проверка до и после hardening-а
- [[CHIPSEC]] — самый глубокий аудит прошивок
- [[AUTOSPLOIT]] — проверка "пробиваемости" текущей защиты
- [[APPLICATIONINSPECTOR]] — анализ безопасности кода
- [[CERTIFICATES]] — управление сертификатами
