import asyncio
import logging
from typing import List, Dict
from models.schemas import FileTask, PipelineResult, AnalysisMetrics, LLMReview
from agents.reader import DataReader
from agents.analyzer import CodeAnalyzer
from agents.llm import LLMAgent
from agents.scorer import QualityScorer

class MasterOrchestrator:
    """Orchestrates the multi-agent pipeline."""
    
    def __init__(self, threshold: float = 7.0, max_retries: int = 3):
        self.threshold = threshold
        self.max_retries = max_retries
        self.reader = DataReader()
        self.analyzer = CodeAnalyzer()
        self.llm = LLMAgent()
        self.scorer = QualityScorer()
        self.logger = logging.getLogger("Orchestrator")

    async def process_file(self, file_path: str) -> PipelineResult:
        task = FileTask(path=file_path)
        result = PipelineResult(file_path=file_path)
        
        while task.retry_count <= self.max_retries:
            # 1. Read
            code = await self.reader.read(task.path)
            if not code:
                result.status = "FAILED_TO_READ"
                return result
            
            # 2. Analyze
            metrics = self.analyzer.analyze(code)
            result.metrics = metrics
            
            # 3. LLM Review
            review = await self.llm.review(code, task.fail_context)
            result.review = review
            
            # 4. Score
            score = self.scorer.calculate(metrics, review)
            result.quality_score = score
            
            # 5. Verify Gate
            if score >= self.threshold:
                result.status = "SUCCESS"
                return result
            
            # 6. Retry Manager
            task.retry_count += 1
            if task.retry_count <= self.max_retries:
                message = f"Retry {task.retry_count}: Quality score {score:.2f} < {self.threshold}. Issues: {review.issues}"
                self.logger.warning(message)
                task.fail_context.append(message)
            else:
                result.status = "FAILED_THRESHOLD"
        
        return result

    async def run(self, tasks: List[str]) -> List[PipelineResult]:
        # Process all tasks concurrently
        results = await asyncio.gather(*[self.process_file(t) for t in tasks])
        return list(results)
