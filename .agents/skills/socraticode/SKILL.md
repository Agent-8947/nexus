# SocratiCode — Codebase Context Engine [NEXUS Edition]
**Status**: Experimental / Integration
**Engine**: [SocratiCode](https://github.com/giancarloerra/SocratiCode)

## Overview
SocratiCode provides high-fidelity codebase intelligence via hybrid semantic search, polyglot dependency graphs, and symbol-level impact analysis. It runs as an MCP server and is integrated into the NEXUS ecosystem as an advanced code-reasoning skill.

## Tools
This skill exposes the following capabilities:
- `index_codebase`: Start background indexing of the current workspace.
- `search_codebase`: Perform semantic search across indexed files.
- `get_status`: Check indexing progress and system health.
- `visualize_graph`: Generate Mermaid dependency diagrams or interactive HTML maps.
- `impact_analysis`: Trace the blast radius of symbols or files.

## Usage
To use SocratiCode, ensure Docker is running. The skill automatically manages the background MCP server.

### Example
```python
from skills.socraticode.scripts.bridge import SocratiCodeClient

client = SocratiCodeClient()
results = client.search("how is DNA synthesis handled?")
```

## Integration Details
- **Protocol**: MCP (JSON-RPC over Stdio)
- **Database**: Qdrant (Docker)
- **Embeddings**: Ollama (Docker/Local) or Google Gemini API
- **Persistence**: Index data is stored in Docker volumes.
