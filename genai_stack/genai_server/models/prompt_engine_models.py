from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from genai_stack.prompt_engine.utils import PromptTypeEnum


class PromptEngineBaseModel(BaseModel):
    session_id: int
    type: PromptTypeEnum


class PromptEngineSetRequestModel(PromptEngineBaseModel):
    template: str


class PromptEngineSetResponseModel(PromptEngineBaseModel):
    template: str


class PromptEngineGetRequestModel(PromptEngineBaseModel):
    query: str = None
    should_validate: bool = False


class PromptEngineGetResponseModel(PromptEngineBaseModel):
    template: str
