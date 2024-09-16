from fastapi import APIRouter

from genai_stack.constant import API, PROMPT_ENGINE
from genai_stack.genai_server.settings.settings import settings
from genai_stack.genai_server.models.prompt_engine_models import (
    PromptEngineGetRequestModel, PromptEngineGetResponseModel,
    PromptEngineSetRequestModel, PromptEngineSetResponseModel
)
from genai_stack.genai_server.services.prompt_engine_service import PromptEngineService

service = PromptEngineService(store=settings.STORE)

router = APIRouter(prefix=API + PROMPT_ENGINE, tags=["prompt-engine"])


@router.get("/prompt")
def get_prompt(data: PromptEngineGetRequestModel) -> PromptEngineGetResponseModel:
    return service.get_prompt(data=data)


@router.post("/prompt")
def set_prompt(data: PromptEngineSetRequestModel) -> PromptEngineSetResponseModel:
    return service.set_prompt(data=data)
