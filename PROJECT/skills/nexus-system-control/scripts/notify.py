import os
import argparse
import requests
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description="NEXUS Telegram Notifier")
    parser.add_argument("--message", required=True, help="Сообщение для отправки")
    args = parser.parse_args()

    # Загружаем ключи из защищенной папки NEXUS
    env_path = r"e:\Downloads\--ANTIGRAVITY store\--password\.env"
    load_dotenv(env_path)

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_ADMIN_ID")

    if not bot_token or not chat_id:
        print("Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_ADMIN_ID не найдены в секретной папке.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": args.message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Сообщение успешно доставлено (ID: {chat_id}): '{args.message}'")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка отправки: {e}")

if __name__ == "__main__":
    main()
