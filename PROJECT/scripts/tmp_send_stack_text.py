import os
import requests
from pathlib import Path

# Config (Manually copied from .env)
BOT_TOKEN = "8027049517:AAHfsJ418Th7kOJCuDrCLDYEtHvsOjzSPCo"
CHAT_ID = "771386337"

def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=15)
        print(f"Sent chunk {i+1}/{len(chunks)}")

def main():
    stack_file = Path(r"C:\Users\MAC\.gemini\antigravity\brain\30fef173-3eb6-49d6-9b11-ee5fa2b439e2\NEXUS_FULL_STACK.md")
    if stack_file.exists():
        with open(stack_file, "r", encoding="utf-8") as f:
            content = f.read()
            send_message(content)
            print("✅ Done")
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
