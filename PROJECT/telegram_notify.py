"""
NEXUS TELEGRAM NOTIFIER v1.0
Sends text messages and files to a Telegram bot.

Usage:
  python telegram_notify.py --message "Hello"
  python telegram_notify.py --file path/to/file.md
  python telegram_notify.py --file path/to/file.md --message "Caption"
"""
import argparse
import os
import sys
import requests
from pathlib import Path

# --- Configuration ---
# Set these via environment variables or .env file
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

ENV_PATH = Path(__file__).resolve().parent / ".env"


def load_env():
    """Load .env file if it exists."""
    global BOT_TOKEN, CHAT_ID
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key == "TELEGRAM_BOT_TOKEN":
                        BOT_TOKEN = value
                    elif key == "TELEGRAM_CHAT_ID":
                        CHAT_ID = value


def send_message(text: str) -> bool:
    """Send a text message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Telegram has a 4096 char limit per message
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code != 200:
            # Retry without Markdown if parsing fails
            payload["parse_mode"] = ""
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code != 200:
                print(f"[!] Telegram API error (chunk {i+1}): {resp.status_code} — {resp.text}")
                return False
        print(f"  ✓ Sent chunk {i+1}/{len(chunks)}")
    
    return True


def send_file(file_path: str, caption: str = "") -> bool:
    """Send a file via Telegram Bot API."""
    path = Path(file_path)
    if not path.exists():
        print(f"[!] File not found: {path}")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    with open(path, "rb") as f:
        files = {"document": (path.name, f)}
        data = {"chat_id": CHAT_ID}
        if caption:
            data["caption"] = caption[:1024]  # Telegram caption limit
            data["parse_mode"] = "Markdown"
        
        resp = requests.post(url, data=data, files=files, timeout=30)
    
    if resp.status_code != 200:
        print(f"[!] Telegram API error: {resp.status_code} — {resp.text}")
        return False
    
    return True


def main():
    load_env()
    
    if not BOT_TOKEN or not CHAT_ID:
        print("═══ NEXUS TELEGRAM NOTIFIER ═══")
        print("[!] Missing credentials.")
        print(f"    Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in:")
        print(f"    {ENV_PATH}")
        print()
        print("    Example .env file:")
        print('    TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."')
        print('    TELEGRAM_CHAT_ID="your_chat_id"')
        print()
        print("    To get your chat_id, message @userinfobot on Telegram.")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="NEXUS Telegram Notifier")
    parser.add_argument("--message", "-m", type=str, help="Text message to send")
    parser.add_argument("--file", "-f", type=str, help="File to send")
    args = parser.parse_args()
    
    if not args.message and not args.file:
        print("[!] Specify --message and/or --file")
        sys.exit(1)
    
    print("═══ NEXUS TELEGRAM NOTIFIER ═══")
    
    success = True
    
    if args.file:
        print(f"  Sending file: {Path(args.file).name}...")
        caption = args.message or ""
        if send_file(args.file, caption):
            print(f"  ✅ File delivered.")
        else:
            success = False
    elif args.message:
        print(f"  Sending message ({len(args.message)} chars)...")
        if send_message(args.message):
            print(f"  ✅ Message delivered.")
        else:
            success = False
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
