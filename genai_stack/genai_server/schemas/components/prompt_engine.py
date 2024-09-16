from sqlalchemy import Column, Integer, JSON, ForeignKey, Enum, String

from genai_stack.genai_server.schemas.base_schemas import TimeStampedSchema
from genai_stack.prompt_engine.utils import PromptTypeEnum


class PromptSchema(TimeStampedSchema):
    """
    Schema for the Prompt model
    """

    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stack_session = Column(
        Integer, ForeignKey("stack_sessions.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(Enum(PromptTypeEnum), default=PromptTypeEnum.SIMPLE_CHAT_PROMPT.value)
    template = Column(String)
    meta_data = Column(JSON, nullable=True)
