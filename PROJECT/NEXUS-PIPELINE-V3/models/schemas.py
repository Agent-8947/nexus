from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class FileTask:
    path: str
    content: Optional[str] = None
    retry_count: int = 0
    fail_context: List[str] = field(default_factory=list)

@dataclass
class AnalysisMetrics:
    loc: int
    complexity: int
    functions_count: int
    classes_count: int
    duplicates_count: int

@dataclass
class LLMReview:
    issues: List[str]
    suggestions: List[str]
    score: float

@dataclass
class PipelineResult:
    file_path: str
    metrics: Optional[AnalysisMetrics] = None
    review: Optional[LLMReview] = None
    quality_score: float = 0.0
    status: str = "PENDING"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
