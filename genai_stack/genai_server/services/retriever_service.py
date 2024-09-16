from fastapi import HTTPException
from sqlalchemy.orm import Session

from genai_stack.genai_platform.services.base_service import BaseService
from genai_stack.genai_server.models.retriever_models import RetrieverResponseModel, RetrieverRequestModel
from genai_stack.genai_server.schemas import StackSessionSchema
from genai_stack.genai_server.utils import get_current_stack
from genai_stack.genai_server.settings.config import stack_config


class RetrieverService(BaseService):

    def retrieve(self, data: RetrieverRequestModel) -> RetrieverResponseModel:
        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            stack = get_current_stack(config=stack_config, engine=session, session=stack_session)
            response = stack.retriever.retrieve(data.query)
            return RetrieverResponseModel(
                output=response['output'],
                session_id=data.session_id,
            )
