from typing import Any, Dict, List

from langchain import document_loaders
from langchain.docstore.document import Document as LangDocument
from langchain.embeddings import OpenAIEmbeddings
import logging

from llm_stack.etl.base import EtlBase
from llm_stack.vectordb.base import BaseVectordb
from llm_stack.utils.importing import import_class
from llm_stack.constants.vectordb import VECTORDB_CONFIG_KEY

logger = logging.getLogger(__name__)

documentloaders_type_to_cls_dict: Dict[str, Any] = {
    documentloader_name: import_class(
        f"langchain.document_loaders.{documentloader_name}",
    )
    for documentloader_name in document_loaders.__all__
}


def list_langchain_loaders():
    return list(
        {documentloader.__name__ for documentloader in documentloaders_type_to_cls_dict.values()}  # noqa: E501
    )


class LangLoaderEtl(EtlBase):
    def __init__(
        self,
        config: str,
        name: str = "LangLoaderEtl",
        vectordb: BaseVectordb = None,
    ) -> None:
        self.vectordb = vectordb
        super().__init__(name=name, config=config)

    def load_from_source(self):
        source = self.config_dict.get("source")
        LoaderCls = import_class(
            f"langchain.document_loaders.{source.get('name')}",
        )
        loader = LoaderCls(**source.get("fields"))
        self.documents = loader.load()
        return self.documents

    def _get_embedding(self):
        destination = self.config_dict.get("destination", {})
        if embedding := destination.get("embedding"):
            embedding_cls = import_class(
                f"langchain.embeddings.{embedding.get('name')}",
            )
            self.embedding = embedding_cls(**embedding.get("fields"))
        elif not self.embedding:
            self.embedding = OpenAIEmbeddings(openai_api_key=embedding.get("openai_api_key", ""))
        return self.embedding

    def load_into_destination(self, source_docs: List[LangDocument]):
        destination = self.config_dict.get(VECTORDB_CONFIG_KEY)

        class_name = destination.get("class_name")
        if not class_name:
            class_name = "llm_stack"
            logger.info(f"Defaulted class name to {class_name}")

        class_name = class_name.capitalize()

        self.vectordb.store_documents(source_docs)
        logger.info("Stored to vectordb")

    def run(self):
        source_docs: List[LangDocument] = self.load_from_source()
        self.load_into_destination(source_docs=source_docs)
