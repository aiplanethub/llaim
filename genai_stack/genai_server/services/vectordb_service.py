from fastapi import HTTPException
from sqlalchemy.orm import Session
from genai_stack.genai_platform.services.base_service import BaseService
from genai_stack.genai_server.models.vectordb_models import (
    DocumentType, RetrieverAddDocumentsRequestModel, RetrieverSearchRequestModel, RetrieverAddDocumentsResponseModel,
    RetrieverSearchResponseModel
)
from genai_stack.genai_server.schemas import StackSessionSchema
from genai_stack.genai_server.utils import get_current_stack
from genai_stack.genai_server.settings.config import stack_config


class VectorDBService(BaseService):

    def add_documents(self, data: RetrieverAddDocumentsRequestModel) -> RetrieverAddDocumentsResponseModel:

        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            stack = get_current_stack(config=stack_config, engine=session, session=stack_session)
            stack.vectordb.add_documents(data.documents)
            return RetrieverAddDocumentsResponseModel(
                documents=[
                    DocumentType(
                        page_content=document.page_content,
                        metadata=document.metadata
                    ) for document in data.documents
                ],
                session_id=data.session_id
            )

    def search(self, data: RetrieverSearchRequestModel) -> RetrieverSearchResponseModel:

        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            stack = get_current_stack(config=stack_config, engine=session, session=stack_session)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            documents = stack.vectordb.search(data.query)
            return RetrieverSearchResponseModel(
                documents=[
                    DocumentType(
                        page_content=document.page_content,
                        metadata=document.metadata
                    ) for document in documents
                ],
                session_id=data.session_id
            )
