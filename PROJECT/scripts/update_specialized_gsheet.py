import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"
FILE_PATH = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru-extended.csv"

# The specific Google Sheet ID provided by the user
TARGET_FILE_ID = "1X6uPvfjGfZy2TFYOCotlvixtGtz7vm6fnoc07d3ntXA"

def update_drive_spreadsheet():
    if not os.path.exists(TOKEN_PATH):
        print(f"[ERROR] Token file not found at {TOKEN_PATH}")
        return

    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload(FILE_PATH, 
                            mimetype='text/csv',
                            resumable=True)
    
    try:
        print(f"[NEXUS] Updating existing Google Sheets document ({TARGET_FILE_ID})...")
        file = service.files().update(fileId=TARGET_FILE_ID,
                                      media_body=media,
                                      fields='id, webViewLink').execute()
        
        print(f"✅ Spreadsheet updated successfully.")
        print(f"✅ Link: {file.get('webViewLink')}")
        
    except Exception as e:
        print(f"❌ Drive Update Failed: {e}")

if __name__ == "__main__":
    update_drive_spreadsheet()
