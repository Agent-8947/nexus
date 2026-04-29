from models.schemas import AnalysisMetrics, LLMReview

class QualityScorer:
    """Calculates final quality score based on metrics and LLM review."""
    
    def calculate(self, metrics: AnalysisMetrics, review: LLMReview) -> float:
        # Formula: (LOC penalty + complexity + llm_score)
        # 1. Complexity penalty: Higher complexity lowers score.
        comp_penalty = min(5.0, metrics.complexity / 10.0)
        
        # 2. LOC penalty: Excessive LOC might lower score (if > 500)
        loc_penalty = max(0.0, (metrics.loc - 500) / 100.0) if metrics.loc > 500 else 0.0
        
        # 3. LLM Score: 0-10 base
        base_score = review.score
        
        # Duplicate penalty
        dup_penalty = min(2.0, metrics.duplicates_count / 5.0)
        
        final_score = base_score - comp_penalty - loc_penalty - dup_penalty
        return max(0.0, min(10.0, final_score))
