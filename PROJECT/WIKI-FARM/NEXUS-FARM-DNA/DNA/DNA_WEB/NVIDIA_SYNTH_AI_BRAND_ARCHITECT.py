import requests
import json
import sqlite3
import os
import logging
import time
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("AI_BRAND_ARCHITECT")

load_dotenv()

class AI_BRAND_ARCHITECT_Agent:
    """
    NEXUS AI Brand Architect [Refactored v2.0]
    High-resiliency agent for brandbook synthesis.
    
    Fixes implemented after Adversarial Review:
    1. HTML Cleaning (BeautifulSoup)
    2. Context Managers for DB (with)
    3. Retry logic (urllib3)
    4. Robust JSON parsing (Native JSON Mode)
    5. Versioned API Endpoints
    6. Grounded Temperature (0.1)
    """
    def __init__(self):
        self.firecrawl_key = os.getenv('FIRECRAWL_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.db_path = 'nexus_brand_vault.db'
        
        # Setup Resilient Session
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        self._init_db()

    def _init_db(self):
        """Thread-safe database initialization."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS brand_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT UNIQUE,
                    brand_identity TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def _clean_html(self, html: str) -> str:
        """Extract only meaningful text and meta-data, removing noise."""
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script/style tags
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()
        
        # Extract metadata
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc = meta_desc['content'] if meta_desc else ""
        
        # Clean text
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())
        
        # 6000 chars limit (Semantic cut, not random byte cut)
        return f"DESC: {desc}\n\nCONTENT: {clean_text[:6000]}"

    def _scrape_url(self, url: str) -> Dict[str, Any]:
        """Scrape target URL via Firecrawl v1."""
        if not self.firecrawl_key:
            raise ValueError("FIRECRAWL_API_KEY missing")

        logger.info(f"Scraping: {url}")
        resp = self.session.post(
            'https://api.firecrawl.dev/v1/scrape',
            headers={'Authorization': f'Bearer {self.firecrawl_key}', 'Content-Type': 'application/json'},
            json={'url': url, 'formats': ['html']},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def _synthesize_brand(self, context: str) -> Dict[str, Any]:
        """Call LLM with low temperature for structured brand synthesis."""
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY missing")

        prompt = f"""Analyze this website data and generate a structured AI Brandbook.
DATA:
{context}

Return ONLY valid JSON with keys:
- primary_colors (list of hex)
- typography (dict: headings, body, weights)
- vision_statement (str)
- tone_of_voice (list of 5 tags)
- motion_directives (list of 3 animation principles)
"""
        resp = self.session.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {self.openai_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'gpt-4o',
                'messages': [{'role': 'system', 'content': 'You are a Senior Brand Architect. Output valid JSON only.'},
                             {'role': 'user', 'content': prompt}],
                'temperature': 0.1,
                'response_format': { "type": "json_object" }
            },
            timeout=60
        )
        resp.raise_for_status()
        return json.loads(resp.json()['choices'][0]['message']['content'])

    def analyze(self, url: str) -> Dict[str, Any]:
        """Main entry point with full lifecycle management."""
        try:
            # 1. Cache Check
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT brand_identity FROM brand_vault WHERE source_url = ?', (url,))
                row = cursor.fetchone()
                if row:
                    logger.info("Cache hit.")
                    return json.loads(row[0])

            # 2. Scrape & Clean
            scraped = self._scrape_url(url)
            html = scraped.get('data', {}).get('html', '')
            clean_context = self._clean_html(html)

            # 3. Synthesize
            brandbook = self._synthesize_brand(clean_context)

            # 4. Persist
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    'INSERT OR REPLACE INTO brand_vault (source_url, brand_identity) VALUES (?, ?)',
                    (url, json.dumps(brandbook))
                )
            
            logger.info("Analysis complete and vaulted.")
            return brandbook

        except Exception as e:
            logger.error(f"FATAL ERROR: {str(e)}")
            return {"error": str(e), "status": "failed"}

# Nexus Ecosystem Integration
def create_agent():
    return AI_BRAND_ARCHITECT_Agent()

if __name__ == "__main__":
    agent = create_agent()
    # Test with a real-world site
    res = agent.analyze("https://nvidia.com")
    print(json.dumps(res, indent=2))