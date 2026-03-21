import requests
from pathlib import Path

# Config
BOT_TOKEN = "8027049517:AAHfsJ418Th7kOJCuDrCLDYEtHvsOjzSPCo"
CHAT_ID = "771386337"

def send_compact_stack():
    compact_file = Path(r"C:\Users\MAC\.gemini\antigravity\brain\30fef173-3eb6-49d6-9b11-ee5fa2b439e2\NEXUS_COMPACT_STACK.md")
    if compact_file.exists():
        with open(compact_file, "r", encoding="utf-8") as f:
            content = f.read()
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": content,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            requests.post(url, json=payload, timeout=15)
            print("✅ Compact Stack sent.")
    else:
        print("File not found.")

if __name__ == "__main__":
    send_compact_stack()
