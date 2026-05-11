# Cheatsheet: AI Engineering Production Rules

## 🧠 Model Selection Logic
- **Simple Logic/Parsing**: Use small models (Gemma 2B, Llama 1B).
- **Creative/Strategic**: Use mid-range (Claude Haiku 4.5, Llama 70B).
- **Master Architect/Judgment**: Use top-tier (Claude Sonnet 4.5, GPT-4o).

## 📝 Prompt Engineering Hacks
- **Few-Shot**: Always provide 2-3 examples for complex tasks.
- **Chain of Thought**: Add "Think step-by-step" for logic.
- **Delimiters**: Use `###` or XML tags `<content>` to separate sections.
- **Roleplay**: Define a specific Archetype (e.g. "You are a Senior Motion Designer").

## 🚀 Deployment Constraints
- **State Management**: Keep agents stateless where possible. Use `memory.json` for persistence.
- **Error Handling**: Implement retries with exponential backoff for API calls.
- **Fallback**: If the primary model fails, fallback to a faster, cheaper model to ensure service continuity.

## 📈 RAG Optimization
- **K-Value**: Start with K=5 retrieved chunks.
- **Context Filtering**: Filter out low-confidence results before feeding to the prompt.
