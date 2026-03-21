import sys
from pathlib import Path

# Подключаем модули из проекта Legal-DevOps
EXTERNAL_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts")
sys.path.append(str(EXTERNAL_ROOT))

try:
    from nexus_mail_listener_v1 import authenticate_gmail, send_reply
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)

def send_full_package():
    print("[NEXUS] Authenticating with Gmail API...")
    service = authenticate_gmail()
    if not service:
        print("[ERROR] Gmail authentication failed.")
        sys.exit(1)

    docs_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\DOCS")
    files_to_send = [
        docs_dir / "Monetization_Vectors.md",
        docs_dir / "10_Ways_To_Earn_With_NEXUS.md",
        docs_dir / "Mechanics_of_Earning.md"
    ]

    valid_files = [str(f) for f in files_to_send if f.exists()]
    
    if not valid_files:
        print("[ERROR] No files found to send.")
        sys.exit(1)

    body = """
Привет!

Я упаковал все наши сегодняшние наработки по монетизации NEXUS. 
Во вложении 3 документа:
1. Monetization_Vectors.md — Основные стратегии.
2. 10_Ways_To_Earn_With_NEXUS.md — Конкретный список из 10 способов со статусом готовности инструментов.
3. Mechanics_of_Earning.md — Подробный разбор экономики и техпроцессов.

Все инструменты (Firecrawl, Intel-Sight, OSINT, Stripe, Telegram) готовы к работе.

Жду твоего выбора направления для запуска первого теста.
"""

    to_email = "yurarulev@gmail.com"
    subject = "NEXUS: ПОЛНЫЙ ПАКЕТ МОНЕТИЗАЦИИ (Стратегии + Механика)"
    
    print(f"[NEXUS] Sending full package to {to_email}...")
    send_reply(service, to_email, subject, body, valid_files)
    print("[SUCCESS] All files sent successfully.")

if __name__ == "__main__":
    send_full_package()
