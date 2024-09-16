from fastapi import HTTPException
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session

from genai_stack.genai_platform.services import BaseService
from genai_stack.genai_server.models.prompt_engine_models import (
    PromptEngineGetRequestModel, PromptEngineGetResponseModel,
    PromptEngineSetRequestModel, PromptEngineSetResponseModel
)
from genai_stack.genai_server.schemas import StackSessionSchema
from genai_stack.genai_server.schemas.components.prompt_engine import PromptSchema
from genai_stack.genai_server.settings.config import stack_config
from genai_stack.genai_server.utils import get_current_stack
from genai_stack.prompt_engine.utils import PromptTypeEnum


class PromptEngineService(BaseService):

    def get_prompt(self, data: PromptEngineGetRequestModel) -> PromptEngineGetResponseModel:
        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            stack = get_current_stack(config=stack_config, engine=session, session=stack_session)
            prompt = stack.prompt_engine.get_prompt_template(promptType=data.type, query=data.query)
            return PromptEngineGetResponseModel(
                template=prompt.template,
                session_id=data.session_id,
                type=data.type.value
            )

    def set_prompt(self, data: PromptEngineSetRequestModel) -> PromptEngineSetResponseModel:
        with Session(self.engine) as session:
            stack_session = session.get(StackSessionSchema, data.session_id)
            if stack_session is None:
                raise HTTPException(status_code=404, detail=f"Session {data.session_id} not found")
            input_variables = ["context", "history", "query"]
            if data.type.value == PromptTypeEnum.SIMPLE_CHAT_PROMPT.value:
                input_variables.remove("context")
            elif data.type.value == PromptTypeEnum.CONTEXTUAL_QA_PROMPT.value:
                input_variables.remove("history")
            for variable in input_variables:
                if variable not in data.template:
                    raise HTTPException(status_code=400, detail=f"Input variable {variable} not found in template")
            for variable in data.template.split("{"):
                if "}" in variable and variable.split("}")[0] not in input_variables:
                    raise HTTPException(status_code=400, detail=f"Unknown input variable {variable.split('}')[0]}")
            prompt_session = (
                session.query(PromptSchema)
                .filter_by(stack_session=data.session_id, type=data.type.value)
                .first()
            )
            if prompt_session is not None:
                prompt_session.template = data.template
                session.commit()
            else:
                prompt_session = PromptSchema(
                    stack_session=data.session_id,
                    type=data.type.value,
                    template=data.template,
                    meta_data={}
                )
                session.add(prompt_session)
                session.commit()
            return PromptEngineSetResponseModel(
                template=prompt_session.template,
                session_id=data.session_id,
                type=data.type.value
            )
