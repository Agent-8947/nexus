import os
from langchain_community.graphs import FalkorDBGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain.chains import GraphQAChain

class NexusGraphRAG:
    def __init__(self, host="127.0.0.1", port=6380, graph_name="nexus_wiki"):
        """
        Connects to FalkorDB running in Docker.
        Requires OPENAI_API_KEY environment variable.
        """
        print(f"Connecting to FalkorDB at {host}:{port}...")
        self.graph = FalkorDBGraph(database=graph_name, host=host, port=port)
        
        # Initialize LLM for both Extraction and QA
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

        # LLMGraphTransformer extracts entities and relationships from raw text
        self.transformer = LLMGraphTransformer(
            llm=self.llm,
            allowed_nodes=["Agent", "Brand", "Skill", "Architecture", "Technology"],
            allowed_relationships=["MODIFIES", "USES", "PART_OF", "ORCHESTRATES", "GENERATES"]
        )

    def ingest_text(self, text: str):
        """
        Parses unstructured text, extracts knowledge graph, and saves it to FalkorDB.
        """
        from langchain_core.documents import Document
        
        print("Extracting Graph Entities and Relationships via LLM...")
        documents = [Document(page_content=text)]
        graph_documents = self.transformer.convert_to_graph_documents(documents)
        
        print(f"Adding {len(graph_documents[0].nodes)} nodes and {len(graph_documents[0].relationships)} edges to FalkorDB...")
        self.graph.add_graph_documents(graph_documents)
        return "Ingestion Complete."

    def query(self, question: str):
        """
        Queries the FalkorDB knowledge graph directly to answer the question.
        """
        print(f"Querying Knowledge Graph: '{question}'")
        chain = GraphQAChain.from_llm(self.llm, graph=self.graph, verbose=True)
        return chain.invoke(question)

if __name__ == "__main__":
    # Test block
    print("NexusGraphRAG Engine Ready.")
    # test_rag = NexusGraphRAG()
    # test_rag.ingest_text("Agent NVIDIA_SYNTH_AI_BRAND_ARCHITECT modifies the Brand Solara by generating SVG layouts.")
    # print(test_rag.query("Which agent modifies the Solara brand?"))
