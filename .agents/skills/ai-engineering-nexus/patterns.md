# AI Engineering Patterns & Blueprints

## 🔄 The Reflection Loop (Agent Reliability)
**When to use**: Critical tasks (Code generation, Brandbook synthesis).
**Mechanism**:
1. **Initial Draft**: Agent generates content based on promp.
2. **Critique Pass**: A secondary prompt asks the agent to find 3 flaws.
3. **Revision**: Agent rewrite content fixing the flaws.
**Goal**: Zero-hallucination and logical consistency.

## 📥 Advanced RAG (Retrieval Optimization)
**When to use**: High-context projects (NEXUS WIKI, DNA Library).
**Blueprint**:
- **Preprocessing**: Chunking by semantic section, not just tokens.
- **Reranking**: Use a Cross-Encoder to rank the top 5 results for relevance before feeding to the LLM.
- **Context Injection**: Use metadata (author, date, tags) to bias retrieval.

## 🧩 Microservices for AI
**When to use**: Scalable deployments (Solara Factory).
**Architecture**:
- **API Gateway**: Handles auth and rate limiting.
- **Logic Service**: Manages the agent workflow.
- **Inference Service**: Dedicated hardware (NVIDIA/Bedrock) for model calls only.
- **Result Bus**: Shared memory for async agent communication.

## 🧪 AI-as-a-Judge (Automated QA)
**When to use**: Measuring quality at scale.
**Logic**: Define a rubric (0-10) for 5 dimensions (Correctness, Tone, Structure, Latency, Safety). Use a stronger model (e.g. Sonnet 4.5) to judge a faster model's output.
