# LEX-NEXUS 05: LAW OF ATOMIC MODULARITY
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: CODE
**Derived from**: [PythonRobotics, JavaScript-Algorithms, Clean-Code-JavaScript]

### 1. DIRECTIVE
Каждый алгоритм, модуль или утилита, генерируемая агентом NEXUS, обязана быть атомарной: один файл = одна ответственность, с единственной точкой входа `run(target) -> dict`. Функция делает ровно одну вещь (Single Responsibility Principle). Запрещено создавать монолитные скрипты, где парсинг, бизнес-логика и вывод перемешаны в одном файле.

**Обоснование:** PythonRobotics (24k stars) содержит 50+ реализаций алгоритмов (Dijkstra, A*, EKF, RRT, SLAM), и каждый — это **отдельный самодостаточный Python-файл** с минимальными зависимостями (numpy, scipy, matplotlib). JavaScript-Algorithms (192k stars) применяет ту же архитектуру: каждый алгоритм в отдельной папке со своим README и тестами. Clean-Code-JavaScript (92k stars) формализует это как правило "Functions should do one thing".

### 2. SYMMETRY / PATTERN

**VIOLATION (Монолитный агент):**
```python
# 800 строк: тут и парсинг CSV, и вызов LLM, и запись в файл
def main():
    data = pd.read_csv("data.csv")
    for row in data.iterrows():
        result = llm.ask(row)
        with open("output.md", "a") as f:
            f.write(result)
```

**COMPLIANCE (Атомарная архитектура):**
```
PROJECT/MODULE/
├── parser.py      # parse(filepath) -> list[dict]
├── analyzer.py    # analyze(data: list[dict]) -> AnalysisResult
├── writer.py      # write(result: AnalysisResult, output_path: str)
└── main.py        # Оркестрация: parse -> analyze -> write
```
