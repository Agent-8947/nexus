import pytest
import asyncio
from agents.analyzer import CodeAnalyzer
from core.orchestrator import MasterOrchestrator

@pytest.mark.asyncio
async def test_analyzer_loc():
    analyzer = CodeAnalyzer()
    code = "def test():\n    print(1)\n"
    metrics = analyzer.analyze(code)
    assert metrics.loc == 2
    assert metrics.functions_count == 1

@pytest.mark.asyncio
async def test_orchestrator_threshold():
    # Mocking or using small test
    orchestrator = MasterOrchestrator(threshold=9.0)
    # This should fail if score is low
    # We can't easily test LLM without API key, but we can test logic
    assert orchestrator.threshold == 9.0
