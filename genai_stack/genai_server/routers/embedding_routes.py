from fastapi import APIRouter

from genai_stack.constant import API, EMBEDDING
from genai_stack.genai_server.settings.settings import settings
from genai_stack.genai_server.models.embedding_models import EmbeddingResponseModel, EmbeddingRequestModel
from genai_stack.genai_server.services.embedding_service import EmbeddingService

service = EmbeddingService(store=settings.STORE)

router = APIRouter(prefix=API + EMBEDDING, tags=["embedding"])


@router.post("/embed-text")
def retrieve(data: EmbeddingRequestModel) -> EmbeddingResponseModel:
    return service.embed_text(data)
