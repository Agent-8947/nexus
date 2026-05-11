import os
import requests
import json
from dotenv import load_dotenv

# Загружаем конфигурацию
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class NexusEmailAgent:
    """
    Интеграционный агент NEXUS для работы с EmailFlare.
    Обеспечивает отправку отчетов и уведомлений через Cloudflare.
    """
    
    def __init__(self):
        self.api_url = f"http://localhost:{os.getenv('PORT', '8090')}/v1"
        self.admin_token = os.getenv('ADMIN_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }

    def send_email(self, to, subject, html_content=None, text_content=None, from_email=None):
        """
        Отправка email через API EmailFlare.
        """
        payload = {
            "to": to,
            "subject": subject,
            "from": from_email,
            "html": html_content,
            "text": text_content
        }
        
        # Удаляем пустые значения
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            response = requests.post(f"{self.api_url}/send", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "status_code": getattr(response, 'status_code', None)}

    def check_status(self):
        """
        Проверка доступности сервиса EmailFlare.
        """
        try:
            # Пытаемся получить список доменов (требуется ADMIN_TOKEN)
            response = requests.get(f"{self.api_url}/domains", headers=self.headers)
            return response.status_code == 200
        except:
            return False

if __name__ == "__main__":
    # Тестовый запуск
    agent = NexusEmailAgent()
    print(f"EmailFlare Status: {'ONLINE' if agent.check_status() else 'OFFLINE (or unconfigured)'}")
