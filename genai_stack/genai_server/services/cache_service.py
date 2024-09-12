from fastapi import HTTPException
from sqlalchemy.orm import Session

from genai_stack.genai_platform.services import BaseService
from genai_stack.genai_server.models.cache_models import GetCacheRequestModel, SetCacheRequestModel, CacheResponseModel
from genai_stack.genai_server.settings.config import stack_config
from genai_stack.genai_server.utils import get_current_stack
from genai_stack.genai_store.schemas import StackSessionSchema


class LLMCacheService(BaseService):

    def get_cache(self, data: GetCacheRequestModel) -> CacheResponseModel:
        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            stack = get_current_stack(config=stack_config, session=stack_session)
            response = stack.llm_cache.get_cache(
                query=data.query,
                metadata=data.metadata
            )
            return CacheResponseModel(
                session_id=data.session_id,
                query=data.query,
                metadata=data.metadata,
                response=response
            )

    def set_cache(self, data: SetCacheRequestModel) -> CacheResponseModel:
        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            stack = get_current_stack(config=stack_config, session=stack_session)
            stack.llm_cache.set_cache(
                query=data.query,
                response=data.response,
                metadata=data.metadata
            )
            return CacheResponseModel(
                session_id=data.session_id,
                query=data.query,
                metadata=data.metadata,
                response=data.response
            )
