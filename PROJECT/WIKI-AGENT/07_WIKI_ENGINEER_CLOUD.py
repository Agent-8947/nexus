import os
import csv
import random
import time
import itertools
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
INVENTIONS_DIR = PROJECT_ROOT / "PROJECT" / "INVENTIONS"
CSV_REPORT = INVENTIONS_DIR / "nexus_blueprints.csv"

TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"
SHEET_NAME = "NEXUS_Engineer_Blueprints"

# Убраны Анимация и Дата-Саенс по запросу. Оставлен чистый Legal-DevOps.
FOCUS_DOMAINS = {
    "PROGRAMMING": ["architecture", "compiler", "framework", "performance", "rust", "go", "python", "js", "typescript", "c++"],
    "OSINT": ["reconnaissance", "scrape", "cybersecurity", "intelligence", "footprint", "crawler", "detect"],
    "LEGAL": ["compliance", "contract", "license", "blockchain", "audit", "policy", "law", "jurisprudence"]
}

IDEA_TEMPLATES = {
    ("OSINT", "LEGAL"): "Судебный Радар. Автоматизирует сбор OSINT информации по цели и валидирует ее ценность как улики по протоколам комплаенса. Базируется на гибриде [{}] и [{}].",
    ("OSINT", "PROGRAMMING"): "Legal-DevOps Crawler. Сверхбыстрый парсер закрытых/открытых реестров для корпоративной разведки. Мультипоточная архитектура: [{}] + [{}].",
    ("LEGAL", "PROGRAMMING"): "Smart Contract & License Auditor. Сканер ИТ-инфраструктуры компаний, проверяющий нарушения лицензионной чистоты в коде (GPL, MIT). Построен на [{}] + [{}]."
}

class NexusEngineerLoop:
    def __init__(self):
        print(f"\n==================================================")
        print(f"  NEXUS LEGAL-DEVOPS ENGINEER [LOOP MODE]")
        print(f"  Domains: OSINT | PROGRAMMING | JURISPRUDENCE")
        print(f"==================================================\n")
        
        INVENTIONS_DIR.mkdir(parents=True, exist_ok=True)
        self.knowledge_base = {}
        self.file_id = None
        self.service = self._init_drive()

    def _init_drive(self):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
            service = build('drive', 'v3', credentials=creds)
            results = service.files().list(q=f"name='{SHEET_NAME}' and trashed=false", spaces='drive', fields='files(id, name)').execute()
            items = results.get('files', [])
            if items:
                self.file_id = items[0]['id']
                print(f"✅ Таблица найдена: {self.file_id}")
            return service
        except Exception as e:
            print(f"❌ Ошибка авторизации Drive: {e}")
            return None

    def _read_dna(self):
        self.knowledge_base.clear()
        valid_repos = [d for d in WIKI_DIR.iterdir() if d.is_dir() and d.name != "__pycache__"]
        for repo in valid_repos:
            for rc in ["README.md", "README", "readme.md", "README.rst", "ARCHITECTURE.md"]:
                if (repo / rc).exists():
                    try:
                        self.knowledge_base[repo.name] = (repo / rc).read_text(encoding="utf-8", errors="ignore")[:3000]
                        break
                    except:
                        pass

    def _analyze(self):
        tagged = {k: [] for k in FOCUS_DOMAINS.keys()}
        for repo_name, content in self.knowledge_base.items():
            content_lower = content.lower()
            for domain, keywords in FOCUS_DOMAINS.items():
                if any(kw in content_lower for kw in keywords):
                    tagged[domain].append(repo_name)
        
        fallbacks = {"PROGRAMMING": ["Go-Core", "Rust-Backend"], "OSINT": ["Recon-Engine", "SpiderFoot"], "LEGAL": ["Smart-Contract-Auditor", "LexData"]}
        for k in tagged:
            if not tagged[k]:
                tagged[k] = fallbacks[k]
        return tagged

    def _generate_strict_legal_devops(self, tagged):
        inventions = []
        domains = list(FOCUS_DOMAINS.keys())
        pairs = list(itertools.combinations(domains, 2))
        
        for d1, d2 in pairs:
            desc_template = IDEA_TEMPLATES.get((d1, d2)) or IDEA_TEMPLATES.get((d2, d1))
            tech1 = random.choice(tagged[d1])
            tech2 = random.choice(tagged[d2])
            fullname = f"{d1}-{d2}-CoreX".replace("_", "")
            final_desc = desc_template.format(tech1, tech2)
            
            inventions.append({
                "Дата": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Категория": f"{d1} + {d2}",
                "Имя Инструмента": fullname,
                "Архитектура (Технологии)": f"{tech1} + {tech2}",
                "Описание Применения": final_desc
            })
        return inventions

    def _upload_drive(self):
        if not self.service: return
        media = MediaFileUpload(str(CSV_REPORT), mimetype='text/csv')
        try:
            if self.file_id:
                self.service.files().update(fileId=self.file_id, media_body=media).execute()
            else:
                file_metadata = {'name': SHEET_NAME, 'mimeType': 'application/vnd.google-apps.spreadsheet'}
                file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                self.file_id = file.get('id')
            print(f"  ☁️ Drive Sync: ОСИНТ-Легал Таблица успешно обновлена.")
        except Exception as e:
            print(f"  ❌ Ошибка загрузки: {e}")

    def loop_agent(self):
        generation_cycle = 1
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Запуск Цикла #{generation_cycle}")
            
            self._read_dna()
            tagged = self._analyze()
            ideas = self._generate_strict_legal_devops(tagged)
            
            file_exists = CSV_REPORT.exists()
            with open(CSV_REPORT, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Дата", "Категория", "Имя Инструмента", "Архитектура (Технологии)", "Описание Применения"])
                if not file_exists:
                    writer.writeheader()
                for i in ideas:
                    writer.writerow(i)
                    print(f"  💡 {i['Категория']}: {i['Архитектура (Технологии)']}")
                    
            self._upload_drive()
            
            print(f"⏳ Ждём 60 секунд. Данные ушли в защитный контур...")
            generation_cycle += 1
            time.sleep(60)

if __name__ == "__main__":
    NexusEngineerLoop().loop_agent()
