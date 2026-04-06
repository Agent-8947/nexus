import os
import json
import time
import logging
from pathlib import Path
from collections import Counter

logging.basicConfig(level=logging.INFO, format='📚 [ARCHIVIST] %(message)s')

# ==========================================
# КОНФИГУРАЦИЯ NEXUS ARCHIVIST
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
BRAIN_INDEX_FILE = PROJECT_ROOT / "PROJECT" / "WIKI" / "nexus_global_brain.json"

# Экспертная система классификации (Expert System Rules)
KNOWLEDGE_TAXONOMY = {
    "OSINT": ["recon", "scraper", "crawler", "shodan", "osint", "leak", "telegram", "twitter", "intelligence", "footprint"],
    "CRYPTO": ["encryption", "hash", "jwt", "blockchain", "ethereum", "wallet", "crypto", "aes", "rsa", "zero-knowledge"],
    "FORECASTING": ["time-series", "predict", "forecast", "prophet", "arima", "regression", "xgboost", "lstm"],
    "PSYCHOLOGY": ["sentiment", "cognitive", "behavior", "nlp", "emotion", "expression", "psych", "text-classification"],
    "MACHINE_LEARNING": ["pytorch", "tensorflow", "tensor", "model", "neural", "train", "dataset", "llm", "transformer"],
    "LEGAL": ["compliance", "license", "audit", "law", "jurisprudence", "contract", "smart-contract", "gdpr", "policy"],
    "INFRASTRUCTURE": ["docker", "kubernetes", "cloud", "aws", "deploy", "ci-cd", "microservice", "rust", "go", "c++", "system"]
}

USE_CASES = {
    "OSINT": "Извлечение цифровых следов и разведка по закрытым/открытым базам для сбора улик.",
    "CRYPTO": "Анализ защищенных данных, аудит смарт-контрактов, деанонимизация блокчейн-транзакций.",
    "FORECASTING": "Построение математических моделей для предсказания корпоративных и финансовых рисков.",
    "PSYCHOLOGY": "Анализ тональности переписок и цифрового следа для когнитивного профайлинга объектов.",
    "MACHINE_LEARNING": "Ядро для обучения локальных нейросетей-аудиторов (Zero-Leak).",
    "LEGAL": "Прямая автоматизация комплаенса и выявления нарушений законодательства/лицензий.",
    "INFRASTRUCTURE": "Высоконагруженный фундамент для запуска других модулей."
}

class NexusArchivist:
    def __init__(self):
        self.global_brain = {}
        if BRAIN_INDEX_FILE.exists():
            try:
                self.global_brain = json.loads(BRAIN_INDEX_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass

    def _extract_readme_context(self, repo_path):
        """Извлекает 3000 символов из README"""
        for rc in ["README.md", "README.rst", "README", "readme.md"]:
            target = repo_path / rc
            if target.exists():
                try:
                    return target.read_text(encoding="utf-8", errors="ignore")[:3000].lower()
                except:
                    return ""
        return ""

    def index_repository(self, repo_path):
        """Интеллектуальный анализ директории"""
        repo_name = repo_path.name
        readme_text = self._extract_readme_context(repo_path)
        
        # 1. Распознавание стека и доменов
        detected_domains = []
        for domain, keywords in KNOWLEDGE_TAXONOMY.items():
            if any(kw in readme_text for kw in keywords):
                detected_domains.append(domain)
                
        if not detected_domains:
            detected_domains = ["UNCATEGORIZED_TOOL"]

        # 2. Оформление перспектив использования
        perspectives = [USE_CASES.get(d, "Интеграция в общую логику исполнения.") for d in detected_domains]

        # 3. Формирование Досье
        dossier = {
            "name": repo_name,
            "indexed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "domains": detected_domains,
            "core_identity": f"Инструмент на стыке: {' + '.join(detected_domains)}",
            "legal_devops_perspective": " | ".join(perspectives),
            "readiness": "LOCAL_AVAILABLE"
        }
        
        # Запись локального файла
        dossier_path = repo_path / "ARCHIVIST_DOSSIER.json"
        dossier_path.write_text(json.dumps(dossier, indent=4, ensure_ascii=False), encoding="utf-8")
        
        # Инъекция в Глобальный Мозг
        self.global_brain[repo_name] = dossier
        return detected_domains

    def run_indexing_loop(self):
        logging.info("👁️ Архивариус просыпается. Начинаю аудит WIKI-библиотеки...")
        
        scanned_count = 0
        new_count = 0
        
        if not WIKI_DIR.exists():
            logging.error("WIKI директория не найдена.")
            return

        for rm_dir in WIKI_DIR.iterdir():
            if not rm_dir.is_dir() or rm_dir.name == "__pycache__":
                continue
                
            scanned_count += 1
            if rm_dir.name not in self.global_brain:
                domains = self.index_repository(rm_dir)
                logging.info(f"➕ Изучен узел: {rm_dir.name} -> Домены: {domains}")
                new_count += 1
                
        # Сохранение Глобального Мозга
        BRAIN_INDEX_FILE.write_text(json.dumps(self.global_brain, indent=4, ensure_ascii=False), encoding="utf-8")
        logging.info(f"🧠 Аудит завершен. Всего в Мозге: {len(self.global_brain)} узлов. Новых знаний: {new_count}")

if __name__ == "__main__":
    while True:
        Archivist = NexusArchivist()
        Archivist.run_indexing_loop()
        logging.info("💤 Архивариус переваривает знания. Следующий обход через 10 минут...")
        time.sleep(600)
