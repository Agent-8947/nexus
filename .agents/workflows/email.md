---
description: Управление рассылками через EmailFlare [NEXUS Edition]
---
// turbo-all

1. Проверка статуса контейнера EmailFlare.

```powershell
docker-compose -f PROJECT/emailflare/docker-compose.yaml ps
```

2. Запуск сервиса (если выключен).

```powershell
docker-compose -f PROJECT/emailflare/docker-compose.yaml up -d
```

3. Отправка тестового отчета NEXUS.

```powershell
python PROJECT/emailflare/nexus_email_agent.py
```

4. Логи рассылки.

```powershell
docker-compose -f PROJECT/emailflare/docker-compose.yaml logs --tail=20
```
