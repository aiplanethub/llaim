from pydantic import BaseModel


class BaseCacheRequestModel(BaseModel):
    session_id: int
    query: str
    metadata: dict = None


class GetCacheRequestModel(BaseCacheRequestModel):
    pass


class SetCacheRequestModel(BaseCacheRequestModel):
    response: str


class CacheResponseModel(BaseCacheRequestModel):
    response: str
