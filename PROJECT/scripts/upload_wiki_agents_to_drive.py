import os
from pathlib import Path
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
DATA_FILE = PROJECT_ROOT / "PROJECT" / "scripts" / "wiki_agents_list.txt"
TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"
DOC_NAME = "NEXUS_WIKI_AGENT_REGISTRY"

AGENT_REGISTRY = """# 🤖 NEXUS Wiki Agents Registry [Numbered Edition]
Generated: {timestamp}

Ниже приведен список активных автономных агентов, управляющих интеллектуальной фабрикой NEXUS Wiki, с цифровой адресацией.

| ID | Агент (Файл) | Специализация | Миссия / Возможности |
|:---:|:--- |:--- |:--- |
| **01** | `01_WIKI_PRIME.py` | Глобальная инсоляция | Массовый импорт репозиториев (380+ целей). Адаптивное клонирование. |
| **02** | `02_WIKI_BULK_INGESTOR.py` | Трафик-инженер | Высоконагруженная синхронизация больших объемов данных. |
| **03** | `03_WIKI_AUTOPILOT.py` | Оперативный куратор | Быстрая очистка и селективное извлечение знаний. |
| **04** | `04_WIKI_ARCHIVIST.py` | Индексатор-системолог | Классификация знаний по доменам и создание "Глобального Мозга". |
| **05** | `05_WIKI_FUSION.py` | Аналитическая связь | Синтез операционных брифингов и выстраивание цепочек инструментов. |
| **06** | `06_WIKI_ENGINEER.py` | Редактор архитектур | Локальная генерация чертежей новых Legal-DevOps инструментов. |
| **07** | `07_WIKI_ENGINEER_CLOUD.py` | Облачный стратег | Генерация архитектур с внешней синхронизацией в Google Sheets. |
| **08** | `08_WIKI_RESEARCHER.py` | Исследователь-аудитор | Оценка исполнимости (RVI) и аудит рисков (Adversarial Review). |
| **09** | `09_WIKI_TECHNICAL_VISION.py` | Технический визионер | Описание и детальная проработка архитектурных идей в текстовом формате. |
| **10** | `10_WIKI_FUSION_INTEGRATOR.py` | Интегратор-синтетик | Объединение чертежей Инженера (06) в единые мета-системы. |
| **11** | `11_WIKI_CONSTRUCTOR.py` | Проектный строитель | Реализация программных скелетов и развертывание структур (Scaffolding). |
| **12** | `12_WIKI_SORTER.py` | Сортировщик-дворецкий | Автономный клининг и доменная организация WIKI-PROJECT. |

---
*NEXUS Protocol | Zero-Hallucination Execution*
"""

def upload_to_docs():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = AGENT_REGISTRY.format(timestamp=timestamp)
    DATA_FILE.write_text(content, encoding="utf-8")
    
    print(f"[*] Connecting to Google Drive...")
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)
        
        # Check if file exists
        results = service.files().list(q=f"name='{DOC_NAME}' and trashed=false", spaces='drive', fields='files(id, name)').execute()
        items = results.get('files', [])
        
        media = MediaFileUpload(str(DATA_FILE), mimetype='text/plain')
        
        if items:
            file_id = items[0]['id']
            print(f"[*] Updating existing Doc: {file_id}")
            service.files().update(fileId=file_id, media_body=media).execute()
        else:
            print(f"[*] Creating new Doc...")
            file_metadata = {'name': DOC_NAME, 'mimeType': 'application/vnd.google-apps.document'}
            file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
            print(f"✅ Doc created! Link: {file.get('webViewLink')}")
            
        print(f"✅ Sync complete.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    upload_to_docs()
