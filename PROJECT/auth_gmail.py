import os
import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print('Installing dependencies...')
    os.system('pip install google-auth-oauthlib google-api-python-client')
    from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
INFRA_DIR = Path(r"E:\Downloads\--ANTIGRAVITY store\pro-0001_Legal-DevOps_Infrastructure")
ROOT_DEVOPS = INFRA_DIR / "PROJECT" / "LEGAL_DEVOPS" / "scripts"
CREDENTIALS_FILE = ROOT_DEVOPS / "credentials.json"
TOKEN_FILE = ROOT_DEVOPS / "token.json"

def renew_token():
    # Проверка наличия credentials.json
    global CREDENTIALS_FILE
    if not CREDENTIALS_FILE.exists():
        fallback = Path(r"E:\Downloads\--ANTIGRAVITY store\--password\credentials.json")
        if fallback.exists():
            print(f"[NEXUS] credentials.json found in backup: {fallback}")
            CREDENTIALS_FILE = fallback
        else:
            print("[ERROR] credentials.json is missing entirely.")
            sys.exit(1)

    print("\n" + "="*50)
    print("ВНИМАНИЕ: ОЖИДАНИЕ ВВОДА ЧЕЛОВЕКА")
    print("="*50)
    print("1. В вашем браузере сейчас откроется окно Google.")
    print("2. Выберите аккаунт yururulev@gmail.com.")
    print("3. Нажмите 'Продолжить' / 'Разрешить' (Allow).")
    print("="*50 + "\n")
    
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    print("\n✅ [SUCCESS] New token.json saved! Gmail API is authorized.")

if __name__ == '__main__':
    renew_token()
