import enum
from typing import TypedDict


class ValidationResponseDict(TypedDict):
    decision: bool
    reason: str
    response: str


class PromptTypeEnum(enum.Enum):
    SIMPLE_CHAT_PROMPT = "SIMPLE_CHAT_PROMPT"
    CONTEXTUAL_CHAT_PROMPT = "CONTEXTUAL_CHAT_PROMPT"
    CONTEXTUAL_QA_PROMPT = "CONTEXTUAL_QA_PROMPT"
