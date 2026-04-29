import json
import base64
import requests
import time
import os
from pathlib import Path

# Path to the robust Legal-DevOps token
TOKEN_PATH = Path(r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json")
CSV_PATH = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-ru.csv")

def get_valid_token():
    """Returns a valid access token using the NEXUS ROBUST REFRESH protocol."""
    if not TOKEN_PATH.exists():
        print(f"❌ Error: token.json not found at {TOKEN_PATH}")
        return None
    
    with open(TOKEN_PATH, "r") as f:
        data = json.load(f)
    
    # Check if close to expiry
    try:
        # Expected format: 2026-04-03T21:26:04Z
        expiry_struct = time.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%SZ")
        expiry_ts = time.mktime(expiry_struct)
    except:
        expiry_ts = 0

    if time.time() > (expiry_ts - 120):
        print("[NEXUS] Token expired. Performing ROBUST REFRESH...")
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
            new_expiry_ts = time.time() + new_data["expires_in"]
            data["expiry"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(new_expiry_ts))
            
            with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f)
            print("✅ Token refreshed successfully.")
        else:
            print(f"❌ Refresh failed: {res.text}")
            return None
            
    return data["token"]

def upload_to_drive_as_sheet():
    token = get_valid_token()
    if not token:
        return

    print(f"[NEXUS] Initializing Google Drive upload (Multipart)...")
    
    # Metadata for the Google Sheet
    metadata = {
        "name": "Top GitHub Repositories (50k - 500k Stars) - NEXUS-RU",
        "mimeType": "application/vnd.google-apps.spreadsheet"
    }
    
    with open(CSV_PATH, "rb") as f:
        csv_data = f.read()

    # Multipart upload
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
        print(f"✅ SUCCESS! File created: {file_info['name']}")
        print(f"🔗 Link: {file_info['webViewLink']}")
    else:
        print(f"❌ Upload Failed: {res.status_code} - {res.text}")

if __name__ == "__main__":
    upload_to_drive_as_sheet()
