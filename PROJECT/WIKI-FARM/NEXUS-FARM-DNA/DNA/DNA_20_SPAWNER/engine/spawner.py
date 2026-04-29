#!/usr/bin/env python3
"""
NEXUS AGENTIC SPAWNER v2.0 [ANTIGRAVITY CORE]
==============================================
Direct bridge between DNA Blueprint and AI Agent.
"""

import json
import sys
import os
from pathlib import Path

class NexusSpawner:
    def __init__(self, engine_dir: Path):
        self.engine_dir = engine_dir
        self.spawner_root = engine_dir.parent
        self.portal_dir = self.spawner_root / "memory" / "portal"
        self.memory_path = self.spawner_root / "memory" / "lineage.json"
        self.portal_dir.mkdir(parents=True, exist_ok=True)

    def spawn(self, child_json_path: Path):
        with open(child_json_path, 'r', encoding='utf-8') as f:
            child = json.load(f)
            
        child_id = child["child_id"]
        gen = child.get("generation", 0)
        
        # Читаем историю провалов
        history_context = ""
        if self.memory_path.exists():
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            history = [e for e in data.get("lineage", []) if e["child_id"] == child_id]
            if history:
                history_context = f"FAILURES TO FIX: {history[-1].get('failures', [])}"

        # Создаем пакет запроса для Antigravity
        request = {
            "child_id": child_id,
            "generation": gen,
            "traits": child["traits"],
            "context": history_context,
            "instruction": (
                "REQUIREMENTS FOR INDUSTRIAL MASTERPIECE:\n"
                "1. RESOLVE CONTRADICTIONS: If traits contradict (e.g., API interface + Local Cryptography), "
                "you MUST define a clear Architecture Topology (e.g., Distributed Zero-Trust or Local Daemon) BEFORE coding. "
                "Do not build chimeras.\n"
                "2. NO SECURITY THEATER: Real encryption requires proper key separation.\n"
                "3. TRUE FUNCTIONALITY: All ML or logic must drive actual outputs, not serve as decorations.\n"
                "4. ZERO-GUESSING VALIDATION: Code must execute cleanly. Strict exception handling required."
            )
        }
        
        req_file = self.portal_dir / f"REQ_GEN_{gen}_{child_id}.json"
        req_file.write_text(json.dumps(request, indent=2, ensure_ascii=False), encoding='utf-8')
        
        print(f"\n[SPAWNER] Generation {gen} requested.")
        print(f"\033[93m[ANTIGRAVITY_REQUIRED]\033[0m Synthesis needed for: {child_id}")
        print(f"Blueprint: nexus/memory/portal/{req_file.name}")
        
        # В этом режиме spawner сообщает оркестратору, что нужно подождать
        # Но для непрерывности цикла мы можем завершить текущий вызов
        return None  # Оркестратор run.py должен быть готов к паузе

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    spawner = NexusSpawner(Path(__file__).resolve().parent)
    spawner.spawn(Path(sys.argv[1]))
