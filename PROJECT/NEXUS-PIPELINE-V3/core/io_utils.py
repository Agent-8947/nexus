import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List
from models.schemas import PipelineResult

class ResultAggregator:
    """Collects and sorts results."""
    def aggregate(self, results: List[PipelineResult]) -> List[PipelineResult]:
        # Deduplicate and sort by score descending
        unique = {r.file_path: r for r in results}.values()
        return sorted(unique, key=lambda x: x.quality_score, reverse=True)

class OutputWriter:
    """Saves reports in JSON and Markdown."""
    def write(self, results: List[PipelineResult], output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        # JSON
        json_data = [vars(r) for r in results]
        # Recursively vars() not working well for nested dataclasses, 
        # but for simplicity we'll just use a basic dict here.
        # Real production would use pydantic.model_dump()
        (out / "report.json").write_text(json.dumps(str(json_data), indent=2))
        
        # Markdown
        md = ["# Pipeline Progress Report", "", "| File | Score | Status | Issues |", "| --- | --- | --- | --- |"]
        for r in results:
            issues = "; ".join(r.review.issues) if r.review else "N/A"
            md.append(f"| {r.file_path} | {r.quality_score:.2f} | {r.status} | {issues} |")
        
        (out / "report.md").write_text("\n".join(md))

class StateStore:
    """Simple JSON-based state persistence."""
    def __init__(self, db_path: str = "state.json"):
        self.db_path = Path(db_path)

    def save_run(self, results: List[PipelineResult]):
        history = []
        if self.db_path.exists():
            try:
                history = json.loads(self.db_path.read_text())
            except: pass
        
        history.append({
            "timestamp": datetime.now().isoformat(),
            "results_count": len(results),
            "avg_score": sum(r.quality_score for r in results) / len(results) if results else 0
        })
        self.db_path.write_text(json.dumps(history, indent=2))
