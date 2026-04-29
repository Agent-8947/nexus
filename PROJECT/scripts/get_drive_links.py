from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure\PROJECT\LEGAL_DEVOPS\scripts\token.json"

def get_links():
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)
        
        query = "(name='NEXUS_WIKI_AGENT_REGISTRY' or name='NEXUS_Researcher_Audits') and trashed=false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name, webViewLink)').execute()
        items = results.get('files', [])
        
        if not items:
            print("❌ No files found in Drive.")
            return

        for item in items:
            print(f"✅ {item['name']}: {item['webViewLink']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_links()
