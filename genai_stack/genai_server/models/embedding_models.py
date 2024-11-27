from pydantic import BaseModel


class EmbeddingRequestModel(BaseModel):
    text: str
    session_id: int


class EmbeddingResponseModel(BaseModel):
    embedding: list
