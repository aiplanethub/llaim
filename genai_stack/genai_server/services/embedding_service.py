from fastapi import HTTPException
from sqlalchemy.orm import Session

from genai_stack.genai_platform.services import BaseService
from genai_stack.genai_server.routers.embedding_routes import EmbeddingRequestModel, EmbeddingResponseModel
from genai_stack.genai_server.utils import get_current_stack
from genai_stack.genai_server.settings.config import stack_config
from genai_stack.genai_store.schemas import StackSessionSchema


class EmbeddingService(BaseService):

    def embed_text(self, data: EmbeddingRequestModel) -> EmbeddingResponseModel:
        with Session(self.engine) as session:
                stack_session = session.get(StackSessionSchema, data.session_id)
                if stack_session is None:
                    raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
                stack = get_current_stack(config=stack_config, session=stack_session)
                stack.embedding.load()
                return EmbeddingResponseModel(
                    embedding=stack.embedding.embed_text(data.text)
                )
