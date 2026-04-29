import os
import json
import re
from typing import Optional
from anthropic import AsyncAnthropic
from models.schemas import LLMReview

class LLMAgent:
    """Claude API agent for code review."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None

    async def review(self, code: str, fail_context: list = None) -> LLMReview:
        if not self.client:
            return LLMReview(issues=["Error: No API Key"], suggestions=["Set ANTHROPIC_API_KEY"], score=0.0)
            
        system_msg = "You are a senior developer. Review the code and provide a JSON response: {issues: [], suggestions: [], score: 0-10}."
        if fail_context:
            system_msg += f" \nPREVIOUS FAIL REASON: {'; '.join(fail_context)}"
            
        try:
            message = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                system=system_msg,
                messages=[{"role": "user", "content": f"Review this code:\n\n{code}"}]
            )
            # Parse JSON from response
            text = message.content[0].text
            # Simple extractor for json block
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return LLMReview(**data)
            return LLMReview(issues=["Failed to parse JSON"], suggestions=[], score=0.0)
        except Exception as e:
            return LLMReview(issues=[f"API Error: {str(e)}"], suggestions=[], score=0.0)
