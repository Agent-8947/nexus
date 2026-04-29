"""
NEXUS Agent Orchestrator  run_agent.py
========================================
Запускает любого агента по номеру (01-14).
После завершения АВТОМАТИЧЕСКИ вызывает Агента 12 (Архивариус)
для сортировки и индексации результатов.

Использование:
    python run_agent.py 06      # Запустить Инженера
    python run_agent.py 11 <blueprint.md>  # Запустить Строителя с параметром
"""

import sys
import subprocess
from pathlib import Path

AGENT_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-AGENT")

# Реестр агентов: номер -> имя файла и описание
REGISTRY = {
    "01": ("01_WIKI_ORCHESTRATOR.py",    "Главный Оркестратор"),
    "02": ("02_WIKI_CRAWLER.py",         "Краулер"),
    "03": ("03_WIKI_EXTRACTOR.py",       "Экстрактор"),
    "04": ("04_WIKI_ANALYZER.py",        "Анализатор"),
    "05": ("05_WIKI_RANKER.py",          "Ранжировщик"),
    "06": ("06_WIKI_ENGINEER.py",        "Инженер (генератор OSINT)"),
    "07": ("07_WIKI_EXPORTER.py",        "Экспортёр"),
    "08": ("08_WIKI_RESEARCHER.py",      "Исследователь-Аудитор"),
    "09": ("09_WIKI_TECHNICAL_VISION.py","Технический Визионер"),
    "10": ("10_WIKI_FUSION_INTEGRATOR.py","Интегратор-Синтетик"),
    "11": ("11_WIKI_CONSTRUCTOR.py",     "Строитель"),
    "12": ("12_WIKI_SORTER.py",          "Архивариус (Дворецкий)"),
    "13": ("13_WIKI_MARKETER.py",         "Маркетолог (Брендинг + Лендинг)"),
    "14": ("14_WIKI_COPYWRITER.py",        "Копирайтер (Нейминг + Тексты)"),
}

SORTER_SCRIPT = AGENT_DIR / "12_WIKI_SORTER.py"

# Связки: после запуска агента X автоматически запустить Y, Z...
PIPELINES = {
    "06": ["09", "08"],    # Инженер  Визионер  Аудитор
    "11": ["14", "13"],   # Строитель  Копирайтер (нейминг)  Маркетолог (берёт имя)
    "13": ["14"],          # Маркетолог в одиночку тоже зовёт Копирайтера первым
}

def print_banner():
    print("\n" + "=" * 58)
    print("  NEXUS ORCHESTRATOR  Agent Dispatcher")
    print("  Режим: Выполнение + Авто-сортировка (Агент 12)")
    print("=" * 58 + "\n")

def list_agents():
    print("Доступные агенты:")
    for num, (file, desc) in REGISTRY.items():
        exists = "" if (AGENT_DIR / file).exists() else ""
        print(f"  {exists} [{num}] {desc}")

def run(agent_num, extra_args=None):
    if agent_num not in REGISTRY:
        print(f" Агент [{agent_num}] не найден в реестре.")
        list_agents()
        return

    filename, desc = REGISTRY[agent_num]
    script_path = AGENT_DIR / filename

    if not script_path.exists():
        print(f" Файл не найден: {script_path}")
        return

    # --- Запуск основного агента ---
    cmd = ["python", str(script_path)] + (extra_args or [])
    print(f"[] Запуск Агента {agent_num}: {desc}")
    result = subprocess.run(cmd, cwd=str(AGENT_DIR))
    print(f"\n[] Агент {agent_num} завершён (Exit code: {result.returncode})")

    # --- Автоматические связки из PIPELINES ---
    pipeline = PIPELINES.get(agent_num, [])
    for linked_num in pipeline:
        if linked_num in REGISTRY:
            linked_file, linked_desc = REGISTRY[linked_num]
            linked_path = AGENT_DIR / linked_file
            if linked_path.exists():
                print(f"\n[] Авто-связка: Запуск Агента {linked_num} ({linked_desc})...")
                subprocess.run(["python", str(linked_path)], cwd=str(AGENT_DIR))
                print(f"[] Агент {linked_num} завершён.")
            else:
                print(f"[!] Агент {linked_num} пропущен (файл не найден).")

    # --- Агент 12 всегда последний ---
    if agent_num != "12":
        print(f"\n[] Авто-сортировка: Агент 12 (Архивариус)...")
        subprocess.run(["python", str(SORTER_SCRIPT)], cwd=str(AGENT_DIR))

    print("\n Сеанс завершён.\n")

if __name__ == "__main__":
    print_banner()

    if len(sys.argv) < 2:
        print(" Использование: python run_agent.py <номер> [доп. аргументы]")
        print("   Пример: python run_agent.py 06")
        print("   Пример: python run_agent.py 11 path/to/blueprint.md\n")
        list_agents()
        sys.exit(0)

    agent_num = sys.argv[1].zfill(2)  # "6" -> "06", "11" -> "11"
    extra = sys.argv[2:]
    run(agent_num, extra)
