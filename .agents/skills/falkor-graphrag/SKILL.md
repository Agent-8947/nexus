# GraphRAG-SDK Engine [NEXUS Edition]
**Status**: Experimental / Integration
**Engine**: [FalkorDB/GraphRAG-SDK](https://github.com/FalkorDB/GraphRAG-SDK)

## Overview
This skill provides the ability to build, query, and traverse Knowledge Graphs from unstructured text and PDFs (like WIKI-FARM documents). It uses FalkorDB as the graph engine and LiteLLM for routing models.

## Tools
This skill exposes the following capabilities:
- `ingest_document`: Parses text/PDF, extracts entities/relations, and stores them in the graph.
- `finalize_graph`: Deduplicates entities and builds embeddings.
- `graph_completion`: Asks a question against the Knowledge Graph and returns cited, traceable answers.
- `define_schema`: Sets the strict `GraphSchema` (Entity Types, Relation Types) for project-specific context.

## Requirements
- **Docker**: FalkorDB must be running (`docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest`)
- **Python Package**: `graphrag-sdk[litellm,pdf]`

## Example Schema
```python
from graphrag_sdk import GraphSchema, EntityType, RelationType

schema = GraphSchema(
    entities=[
        EntityType(label="Agent", description="An AI Agent in NEXUS"),
        EntityType(label="Brand", description="A brand identity like Solara"),
    ],
    relations=[
        RelationType(label="MODIFIES", description="Modifies DNA or configuration", patterns=[("Agent", "Brand")]),
    ],
)
```
