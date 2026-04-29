import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"
FILE_PATH = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru.csv"

def upload_to_drive():
    if not os.path.exists(TOKEN_PATH):
        print(f"[ERROR] Token file not found at {TOKEN_PATH}")
        return

    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'NEXUS Specialized Intel: Math, Psycho, Planning, Legal (2k-50k) [RU TRANSLATED]',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    
    media = MediaFileUpload(FILE_PATH, 
                            mimetype='text/csv',
                            resumable=True)
    
    try:
        print(f"[NEXUS] Uploading translated dataset to Google Drive...")
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id, webViewLink').execute()
        
        file_id = file.get('id')
        print(f"✅ File uploaded successfully.")
        print(f"✅ Link: {file.get('webViewLink')}")
        
    except Exception as e:
        print(f"❌ Drive Upload Failed: {e}")

if __name__ == "__main__":
    upload_to_drive()
