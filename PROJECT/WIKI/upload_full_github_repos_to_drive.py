import os
import json
import requests
import csv
from pathlib import Path

TOKEN_PATH = Path(r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json")
CSV_PATH = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru.csv")

def get_fresh_token():
    with open(TOKEN_PATH, "r") as f:
        data = json.load(f)
    
    refresh_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": data["client_id"],
        "client_secret": data["client_secret"],
        "refresh_token": data["refresh_token"],
        "grant_type": "refresh_token"
    }
    res = requests.post(refresh_url, data=payload, timeout=15)
    if res.status_code == 200:
        new_data = res.json()
        data["token"] = new_data["access_token"]
        with open(TOKEN_PATH, "w") as f: json.dump(data, f)
        return new_data["access_token"]
    return None

def upload_full_report():
    token = get_fresh_token()
    if not token: return

    print(f"[NEXUS] Uploading Full Report (390 Repos) to Google Drive...")
    
    metadata = {
        "name": "NEXUS Deep Search: GitHub Repos (50k-500k Stars) - Full RU",
        "mimeType": "application/vnd.google-apps.spreadsheet"
    }
    
    with open(CSV_PATH, "rb") as f:
        csv_data = f.read()

    boundary = "-------314159265358979323846"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/related; boundary={boundary}"
    }

    body = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        "Content-Type: text/csv\r\n\r\n"
    ).encode("utf-8") + csv_data + f"\r\n--{boundary}--".encode("utf-8")

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink"
    res = requests.post(url, headers=headers, data=body, timeout=30)
    
    if res.status_code == 200:
        file_info = res.json()
        print(f"✅ SUCCESS! Full Report Link: {file_info['webViewLink']}")
    else:
        print(f"❌ Upload Failed: {res.status_code} - {res.text}")

if __name__ == "__main__":
    upload_full_report()
