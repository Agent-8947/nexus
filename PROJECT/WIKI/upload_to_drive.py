import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

KEY_PATH = r"E:\Downloads\--ANTIGRAVITY store\--password\secrets\gcloud-sa.json"
FILE_PATH = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-ru.csv"
USER_EMAIL = "yururulev@gmail.com"

def upload_to_drive():
    if not os.path.exists(KEY_PATH):
        print(f"[ERROR] Service account key not found at {KEY_PATH}")
        return

    # Scopes for Drive
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'Top GitHub Repositories (50k - 500k Stars) - RU',
        'mimeType': 'application/vnd.google-apps.spreadsheet' # Convert CSV to Google Sheet
    }
    
    media = MediaFileUpload(FILE_PATH, 
                            mimetype='text/csv',
                            resumable=True)
    
    try:
        print(f"[NEXUS] Uploading {FILE_PATH} to Google Drive...")
        file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id, webViewLink').execute()
        
        file_id = file.get('id')
        print(f"✅ File uploaded successfully. File ID: {file_id}")
        
        # Share with user
        print(f"[NEXUS] Sharing with {USER_EMAIL}...")
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': USER_EMAIL
        }
        service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ).execute()
        
        print(f"✅ Shared with {USER_EMAIL}. Link: {file.get('webViewLink')}")
        
    except Exception as e:
        print(f"❌ Drive Upload Failed: {e}")

if __name__ == "__main__":
    upload_to_drive()
