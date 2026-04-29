import os
import httpx
from pathlib import Path
from typing import Optional

class DataReader:
    """Async reader for local files and URLs."""
    
    async def read(self, path: str) -> Optional[str]:
        if path.startswith("http"):
            async with httpx.AsyncClient() as client:
                try:
                    resp = await client.get(path, timeout=10.0)
                    resp.raise_for_status()
                    return resp.text
                except Exception as e:
                    print(f"Error reading URL {path}: {e}")
                    return None
        else:
            p = Path(path)
            if p.exists() and p.is_file():
                return p.read_text(encoding="utf-8", errors="ignore")
            return None
