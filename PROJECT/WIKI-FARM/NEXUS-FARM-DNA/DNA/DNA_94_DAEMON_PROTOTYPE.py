import os
import json
import socket
import logging
from pathlib import Path

# Config
DNA_ROOT = Path("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI-FARM/NEXUS-FARM-DNA/DNA")
LOCK_FILE = DNA_ROOT / "skills-lock.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [DAEMON] %(message)s")
logger = logging.getLogger("NEXUS_DAEMON")

class NexusDaemon:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.skills = self._load_skills()

    def _load_skills(self):
        if not LOCK_FILE.exists():
            return {}
        try:
            with open(LOCK_FILE, "r") as f:
                return json.load(f).get("skills", {})
        except Exception as e:
            logger.error(f"Error loading skills: {e}")
            return {}

    def get_status(self):
        active_count = 0
        for skill_id, info in self.skills.items():
            path = DNA_ROOT / info["path"]
            if path.exists():
                active_count += 1
        
        return {
            "runtime": self.hostname,
            "status": "ONLINE",
            "total_skills": len(self.skills),
            "available_skills": active_count,
            "os": os.name
        }

    def list_capabilities(self):
        print(f"\n--- NEXUS RUNTIME CAPABILITIES [{self.hostname}] ---")
        for skill_id, info in list(self.skills.items())[:20]: # Show first 20
            status = "[OK]" if (DNA_ROOT / info["path"]).exists() else "[XX]"
            print(f"{status} {skill_id:30} | Version: {info.get('version', 'N/A')} | Hash: {info['hash'][:8]}")
        if len(self.skills) > 20:
            print(f"... and {len(self.skills) - 20} more.")

if __name__ == "__main__":
    daemon = NexusDaemon()
    status = daemon.get_status()
    logger.info(f"Runtime Online: {status['runtime']} | Skills: {status['available_skills']}/{status['total_skills']}")
    daemon.list_capabilities()
