import tempfile

VECTORDB_MODULE = "llm_stack.vectordb"
VECTORDB_CONFIG_KEY = "vectordb"


class VectorDB:
    WEAVIATE = "weaviate"
    CHROMADB = "chromadb"


AVAILABLE_VECTORDB_MAPS = {VectorDB.WEAVIATE: "weaviate/Weaviate", VectorDB.CHROMADB: "chromadb/ChromaDB"}
