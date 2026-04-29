import ast
import re
from typing import List
from models.schemas import AnalysisMetrics

class CodeAnalyzer:
    """Static analysis agent using AST."""
    
    def analyze(self, code: str) -> AnalysisMetrics:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return AnalysisMetrics(0, 0, 0, 0, 0)

        loc = len(code.splitlines())
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        # Simple cyclomatic complexity approximation (branches/loops)
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                complexity += 1
                
        # Simple duplicate detection (same non-empty lines)
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        duplicates = len(lines) - len(set(lines))
        
        return AnalysisMetrics(
            loc=loc,
            complexity=complexity,
            functions_count=len(functions),
            classes_count=len(classes),
            duplicates_count=duplicates
        )
