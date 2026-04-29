import os
import csv
import time
import requests
from urllib.parse import quote
from deep_translator import GoogleTranslator

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import logging
logging.basicConfig(level=logging.INFO, format='🌟 %(message)s')

# ==========================================
# КОНФИГУРАЦИЯ NEXUS INTELLIGENCE
# ==========================================
OUTPUT_CSV_PATH = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-phase3-intel-ru.csv"
TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"

GITHUB_TOKEN = "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"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Тематики для парсинга
DOMAINS = {
    "Psychology": ["psychology", "cognitive", "behavioral"],
    "Design": ["design-system", "ui-ux", "graphic-design"],
    "Encryption": ["cryptography", "encryption", "security-tools"],
    "Statistics": ["statistics", "statistical-analysis"],
    "Analysis": ["data-analysis", "data-science"],
    "Forecasting": ["forecasting", "time-series", "predictive-modeling"]
}

STARS_QUERY = "stars:2000..100000"
PAGES_PER_DOMAIN = 3 # 3 страницы по 50 элементов = 150 топ-хитов на каждую тему (итого ~900 репозиториев)

class NexusPhase3Collector:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='ru')
        self.collected_data = []
        self.seen_urls = set()

    def translate_desc(self, text):
        if not text:
            return "Нет описания."
        try:
            return self.translator.translate(text)
        except Exception:
            return text

    def fetch_github_data(self):
        logging.info("🚀 ЗАПУСК ФАЗЫ 3: Глубокий OSINT-сбор по новым доменам...")
        
        for category, tags in DOMAINS.items():
            logging.info(f"\n🔍 Исследуем домен: {category.upper()}")
            
            for tag in tags:
                query = f"topic:{tag} {STARS_QUERY}"
                encoded_q = quote(query)
                
                for page in range(1, PAGES_PER_DOMAIN + 1):
                    url = f"https://api.github.com/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page=50&page={page}"
                    
                    try:
                        resp = requests.get(url, headers=HEADERS, timeout=15)
                        if resp.status_code == 403:
                            logging.info("  ⚠️ GitHub Rate Limit. Ждём 30 сек...")
                            time.sleep(30)
                            continue
                            
                        data = resp.json()
                        items = data.get("items", [])
                        if not items:
                            break
                            
                        for repo in items:
                            clone_url = repo.get("html_url", "")
                            if clone_url in self.seen_urls:
                                continue
                                
                            self.seen_urls.add(clone_url)
                            desc_en = repo.get("description") or ""
                            desc_ru = self.translate_desc(desc_en)
                            
                            self.collected_data.append({
                                "Category": category,
                                "Tag": tag,
                                "Repository": repo.get("name", ""),
                                "Stars": repo.get("stargazers_count", 0),
                                "Language": repo.get("language", "") or "Multi",
                                "Link": clone_url,
                                "Description (EN)": desc_en.replace('\n', ' '),
                                "Description (RU)": desc_ru.replace('\n', ' ')
                            })
                            
                        logging.info(f"  ✅ {tag} (Стр: {page}) -> Найдено {len(items)} баз.")
                        time.sleep(1) # Вежливый интервал API
                    except Exception as e:
                        logging.error(f"  ❌ Ошибка загрузки {tag}: {e}")

        # Сортируем всё по звездам
        self.collected_data.sort(key=lambda x: x["Stars"], reverse=True)
        logging.info(f"\n🎯 СБОР ЗАВЕРШЕН. Уникальных узлов: {len(self.collected_data)}")

    def save_to_csv(self):
        with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            headers = ["Category", "Tag", "Repository", "Stars", "Language", "Link", "Description (EN)", "Description (RU)"]
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.collected_data)
        logging.info(f"💾 Данные сохранены локально в {OUTPUT_CSV_PATH}")

    def upload_to_drive(self):
        logging.info("☁️ Начинаю синхронизацию с Legal-DevOps Google Drive...")
        if not os.path.exists(TOKEN_PATH):
            logging.error(f"❌ Токен не найден: {TOKEN_PATH}")
            return

        creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)

        target_name = "NEXUS_Intel_Phase3_Psycho_Design_Crypto"
        file_metadata = {
            'name': target_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        
        # Обновляем, если есть, иначе создаем
        file_id = None
        try:
            results = service.files().list(q=f"name='{target_name}' and trashed=false", spaces='drive').execute()
            if results.get('files', []):
                file_id = results.get('files')[0]['id']
        except:
            pass

        media = MediaFileUpload(OUTPUT_CSV_PATH, mimetype='text/csv')
        
        try:
            if file_id:
                file = service.files().update(fileId=file_id, media_body=media, fields='webViewLink').execute()
            else:
                file = service.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()
            logging.info(f"✅ УСПЕШНО! Google Таблица готова.")
            logging.info(f"🔗 ССЫЛКА НА ДОКУМЕНТ: {file.get('webViewLink')}")
        except Exception as e:
            logging.error(f"❌ Ошибка выгрузки на Drive: {e}")

if __name__ == "__main__":
    collector = NexusPhase3Collector()
    collector.fetch_github_data()
    collector.save_to_csv()
    collector.upload_to_drive()
