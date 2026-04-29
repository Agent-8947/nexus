from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"
AUDIT_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\INVENTIONS\Researcher_Audits.txt")
DOC_NAME = "NEXUS_Researcher_Audits"

def force_upload():
    print("[*] Connecting to Google Drive (Legal-DevOps account)...")
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)

    # Verify account identity first
    about = service.about().get(fields='user').execute()
    print(f"[✓] Account: {about['user']['emailAddress']}")

    # Check or create the doc
    results = service.files().list(
        q=f"name='{DOC_NAME}' and trashed=false",
        spaces='drive',
        fields='files(id, name, webViewLink)'
    ).execute()
    items = results.get('files', [])

    media = MediaFileUpload(str(AUDIT_FILE), mimetype='text/plain')

    if items:
        file_id = items[0]['id']
        print(f"[*] Updating existing doc: {file_id}")
        service.files().update(fileId=file_id, media_body=media).execute()
        link = items[0]['webViewLink']
    else:
        print("[*] Creating new doc...")
        metadata = {'name': DOC_NAME, 'mimeType': 'application/vnd.google-apps.document'}
        f = service.files().create(body=metadata, media_body=media, fields='id,webViewLink').execute()
        link = f.get('webViewLink')
        file_id = f.get('id')

    # Make it readable by anyone with the link
    service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'}
    ).execute()

    print(f"\n✅ SUCCESS. Document is live:")
    print(f"   {link}")

if __name__ == "__main__":
    force_upload()
