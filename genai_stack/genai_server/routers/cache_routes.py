from fastapi import APIRouter

from genai_stack.constant import API, LLM_CACHE
from genai_stack.genai_server.settings.settings import settings
from genai_stack.genai_server.models.cache_models import (
    GetCacheRequestModel, SetCacheRequestModel, CacheResponseModel
)
from genai_stack.genai_server.services.cache_service import LLMCacheService

service = LLMCacheService(store=settings.STORE)

router = APIRouter(prefix=API + LLM_CACHE, tags=["llm_cache"])


@router.get("/get-cache")
def get_cache(data: GetCacheRequestModel) -> CacheResponseModel:
    return service.get_cache(data=data)


@router.post("/set-cache")
def set_cache(data: SetCacheRequestModel) -> CacheResponseModel:
    return service.set_cache(data=data)
