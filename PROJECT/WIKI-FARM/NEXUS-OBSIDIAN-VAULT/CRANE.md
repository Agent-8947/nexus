---
tags: [nexus-vault, distribution, security, cloud-native, docker, registry]
category: Infrastructure / Container Management
language: Go
github: https://github.com/google/go-containerregistry
---

# CRANE — Container Image Management Utility (Google)

## Описание
**Crane** — это легковесный и сверхбыстрый инструмент командной строки (написан на Go) от **Google** для взаимодействия с реестрами контейнерных образов (Docker Hub, GCR, ECR, GitHub Packages). Главная фишка: Crane **не требует установки Docker** на хосте. Он работает напрямую с API реестров (OCI), позволяя пушить, пуллить, копировать и изменять образы без создания локального демона.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Go (v1.20+) |
| Library | go-containerregistry (GCR) |
| Protocol | OCI (Open Container Initiative) v1.0+ |
| Security | Auth via credentials, helpers, OAuth |
| Format | Docker layers, Config, Manifest |

## Почему это Killer-App
1. **Agent-friendly**— агенты NEXUS могут управлять контейнерами на GitHub без огромного Docker на борту.
2. **Speed**— `crane copy` переносит образ из AWS в Google Cloud напрямую (Cloud-to-Cloud), не скачивая гигабайты на ваш компьютер.
3. **Inspect**— можно посмотреть содержимое образа (файлы, конфиги) без его запуска (безопасно!).
4. **Tagging**— мгновенное переименование тегов в реестре.
5. **Digest Auth**— работа по хэшу (sha256) гарантирует, что образ не был подменен.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Удаленное Управление Контейнерами (Remote OCI Ops). Позволяет NEXUS Deployer-у работать с облаками напрямую.
- **Интеграция:** Модуль NEXUS CI/CD — автоматическая проверка и пересылка образов между реестрами.
- **Ключевое:** Работает внутри маленьких контейнеров или бинарных агентов.

## Пример запуска (CLI)
```bash
# Посмотреть содержимое образа без скачивания
crane ls gcr.io/google-containers/pause

# Скопировать образ из одного реестра в другой (мгновенно)
crane copy library/ubuntu my-registry.io/ubuntu:latest

# Узнать Digest (SHA) образа для безопасности
crane digest nginx:latest
```

## Связанные Репозитории
- [[CONTAINERSSH]] — запуск SSH в контейнерах
- [[AIRFLOW]] — планировщик, запускающий задачи в контейнерах
- [[ALLUXIO]] — кэширование данных для контейнеров
- [[BUILD-YOUR-OWN-X]] — как работает Docker внутри
- [[ATTACKSURFACEANALYZER]] — проверка безопасности контейнеров
