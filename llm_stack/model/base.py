from typing import Any, Optional
from langchain.memory import VectorStoreRetrieverMemory

from llm_stack.model.server import HttpServer
from llm_stack.retriever import BaseRetriever
from llm_stack.constants.model import MODEL_CONFIG_KEY
from llm_stack.config import ConfigLoader


class BaseModel(HttpServer, ConfigLoader):
    module_name = "Model"
    config_key = MODEL_CONFIG_KEY

    def __init__(
        self,
        config: str = None,
        model_path: Optional[str] = None,
        retriever: BaseRetriever = None,
    ):
        self.load(model_path=model_path)
        self.retriever = retriever
        if config:
            ConfigLoader.__init__(self, self.module_name, config=config)
            self.parse_config(self.config_key, getattr(self, "required_fields", None))

    def get_vector_query(self, query_type: str = "similarity"):
        pass

    def get_memory(self):
        vector_store_memory = VectorStoreRetrieverMemory(
            retriever=self.retriever.get_langchain_memory_retriever(), memory_key="chat_history"
        )
        return vector_store_memory

    def load(self, model_path: str):
        self.model = model_path

    def predict(self, query: Any):
        raise NotImplementedError
