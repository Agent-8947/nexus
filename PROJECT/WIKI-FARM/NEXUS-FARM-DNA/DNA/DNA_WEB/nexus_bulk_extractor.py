import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("NEXUS_BULK_EXTRACTOR")

env_path = Path(r"E:\Downloads\--ANTIGRAVITY store\--password\.env")
load_dotenv(dotenv_path=env_path)

FIRECRAWL_KEY = os.getenv("FIRECRAWL_API_KEY")

if not FIRECRAWL_KEY:
    logger.error("FIRECRAWL_API_KEY not found in environment.")
    exit(1)

TARGET_URL = "https://styles.refero.design"
API_BASE = "https://api.firecrawl.dev/v1"

# Target Directory: NEXUS-FARM-DNA/DNA/DNA_DESIGN/
output_dir = Path(__file__).parent.parent / "DNA_DESIGN"
output_dir.mkdir(parents=True, exist_ok=True)

def start_crawl():
    logger.info(f"Initiating crawl job for {TARGET_URL}")
    headers = {"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"}
    payload = {
        "url": TARGET_URL,
        "limit": 200,
        "scrapeOptions": {
            "formats": ["markdown"]
        }
    }
    
    resp = requests.post(f"{API_BASE}/crawl", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise Exception(f"Failed to start crawl: {data}")
    return data["id"]

def poll_crawl(job_id):
    headers = {"Authorization": f"Bearer {FIRECRAWL_KEY}"}
    while True:
        resp = requests.get(f"{API_BASE}/crawl/{job_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        status = data.get("status")
        if status == "completed":
            logger.info("Crawl job completed successfully.")
            return data.get("data", [])
        elif status in ["failed", "cancelled"]:
            logger.error(f"Crawl job failed with status: {status}")
            return []
            
        logger.info(f"Crawl in progress... (Status: {status}). Waiting 15 seconds.")
        time.sleep(15)

def main():
    try:
        job_id = start_crawl()
        logger.info(f"Job ID obtained: {job_id}. Starting polling loop...")
        items = poll_crawl(job_id)
        
        if not items:
            logger.warning("No data retrieved.")
            return

        extracted_count = 0
        for item in items:
            url = item.get("url", "")
            markdown = item.get("markdown", "")
            
            if markdown:
                # Smart extraction: look for H1 in markdown
                slug = None
                for line in markdown.splitlines():
                    if line.startswith("# "):
                        raw_title = line[2:].split("—")[0].strip()
                        slug = "".join(c for c in raw_title if c.isalnum() or c in ('-', '_', ' ')).strip()
                        slug = slug.replace(" ", "_").lower()
                        break
                
                # Fallback to URL slug
                if not slug:
                    url_part = url.strip("/").split("/")[-1]
                    slug = "".join(c for c in url_part if c.isalnum() or c in ('-', '_')).strip()
                
                # Fallback to numbering
                if not slug or "styles" in slug or "index" in slug:
                    slug = f"brand_{extracted_count}"
                    
                file_path = output_dir / f"{slug}.md"
                
                # Anti-overwrite mechanism
                counter = 1
                while file_path.exists():
                    file_path = output_dir / f"{slug}_{counter}.md"
                    counter += 1
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"<!-- Source URL: {url} -->\n\n{markdown}")
                logger.info(f"Saved: {file_path.name}")
                extracted_count += 1
                
        logger.info(f"Extraction complete. Total files saved: {extracted_count}")

    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")

if __name__ == "__main__":
    main()
