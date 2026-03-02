import os
from supabase import create_client, Client

# Environment variables should be loaded from .env
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xyzcompany.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "public-anon-key")

def get_supabase_client() -> Client:
    """
    Returns an initialized Supabase client.
    Note: Provide real credentials in the environment or `.env` file before calling in production.
    """
    if "xyzcompany" in SUPABASE_URL:
        # Prevent crash if env is missing, but log warning
        print("[WARNING] Using placeholder Supabase credentials. Connection will likely fail.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def check_connection() -> bool:
    try:
        sb = get_supabase_client()
        # A simple query to test connection
        sb.table("test_table").select("*").limit(1).execute()
        return True
    except Exception as e:
        print(f"[!] Supabase connection error: {e}")
        return False
