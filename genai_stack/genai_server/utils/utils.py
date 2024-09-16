import string
import random

from langchain.prompts import PromptTemplate

from genai_stack.genai_server.schemas import PromptSchema
from genai_stack.prompt_engine.utils import PromptTypeEnum
from genai_stack.utils import import_class
from genai_stack.enums import StackComponentType
from genai_stack.genai_server.models.session_models import StackSessionResponseModel
from genai_stack.constants import (
    ETL_MODULE,
    AVAILABLE_ETL_LOADERS,
    VECTORDB_MODULE,
    AVAILABLE_VECTORDB_MAPS,
    MEMORY_MODULE,
    AVAILABLE_MEMORY_MAPS,
    LLM_CACHE_MODULE,
    AVAILABLE_LLM_CACHE_MAPS,
    MODELS_MODULE,
    AVAILABLE_MODEL_MAPS,
    EMBEDDING_MODULE,
    AVAILABLE_EMBEDDING_MAPS,
    RETRIEVER_MODULE,
    AVAILABLE_RETRIEVER_MAPS,
    PROMPT_ENGINE_MODULE,
    AVAILABLE_PROMPT_ENGINE_MAPS,
)


components_mappers = {
    StackComponentType.ETL: {"module_name": ETL_MODULE, "available_maps": AVAILABLE_ETL_LOADERS},
    StackComponentType.VECTOR_DB: {"module_name": VECTORDB_MODULE, "available_maps": AVAILABLE_VECTORDB_MAPS},
    StackComponentType.MEMORY: {"module_name": MEMORY_MODULE, "available_maps": AVAILABLE_MEMORY_MAPS},
    StackComponentType.CACHE: {"module_name": LLM_CACHE_MODULE, "available_maps": AVAILABLE_LLM_CACHE_MAPS},
    StackComponentType.MODEL: {"module_name": MODELS_MODULE, "available_maps": AVAILABLE_MODEL_MAPS},
    StackComponentType.EMBEDDING: {"module_name": EMBEDDING_MODULE, "available_maps": AVAILABLE_EMBEDDING_MAPS},
    StackComponentType.PROMPT_ENGINE: {
        "module_name": PROMPT_ENGINE_MODULE,
        "available_maps": AVAILABLE_PROMPT_ENGINE_MAPS,
    },
    StackComponentType.RETRIEVER: {"module_name": RETRIEVER_MODULE, "available_maps": AVAILABLE_RETRIEVER_MAPS},
}


# Getting Component Class
def get_component_class(component_name: str, class_name: str):
    component_mapper = components_mappers.get(component_name)
    module_name = component_mapper["module_name"]
    # ex: genai_stack.vectordb
    cls_name = component_mapper["available_maps"].get(class_name)
    # ex: weaviate/Weaviate
    cls_path = f"{module_name}.{cls_name.replace('/', '.')}"
    # genai_stack.vectordb.weaviate.Weaviate

    cls = import_class(cls_path)

    return cls


# Creating indexes provided by user
def create_indexes(stack, stack_id: int, session_id: int) -> dict:
    components = [StackComponentType.VECTOR_DB, StackComponentType.MEMORY]

    meta_data = {}
    for component in components:
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        index_name = f"{component.value.title()}{random_string}"
        stack.vectordb.create_index(index_name=index_name)
        meta_data[component] = {"index_name": index_name}

    return meta_data


def get_prompt_from_db(session, session_id, stack_config):
    prompt_sessions = (
        session.query(PromptSchema)
        .filter_by(stack_session=session_id)
    )
    prompt_type_map = {
        PromptTypeEnum.SIMPLE_CHAT_PROMPT.value: {
            "field": "simple_chat_prompt_template",
            "input_variables": ["history", "query"]
        },
        PromptTypeEnum.CONTEXTUAL_CHAT_PROMPT.value: {
            "field": "contextual_chat_prompt_template",
            "input_variables": ["context", "history", "query"]
        },
        PromptTypeEnum.CONTEXTUAL_QA_PROMPT.value: {
            "field": "contextual_qa_prompt_template",
            "input_variables": ["context", "query"]
        }
    }
    for prompt_session in prompt_sessions:
        if "prompt_engine" not in stack_config["components"]:
            stack_config["components"]["prompt_engine"] = {
                "name": "PromptEngine",
                "config": {}
            }
        if "config" not in stack_config["components"]["prompt_engine"]:
            stack_config["components"]["prompt_engine"]["config"] = {}
        stack_config["components"]["prompt_engine"]["config"] = {
            **stack_config["components"]["prompt_engine"]["config"],
            prompt_type_map[prompt_session.type.value]["field"]: PromptTemplate(
                template=prompt_session.template,
                input_variables=prompt_type_map[prompt_session.type.value]["input_variables"]
            )
        }
    return stack_config


def get_current_stack(
    config: dict,
    engine=None,
    session=None,
    default_session: bool = True,
    overide_config: dict = None
):
    if engine is not None:
        config = get_prompt_from_db(
            session=engine,
            session_id=session.id,
            stack_config=config
        )
    components = {}
    if session is None and default_session:
        from genai_stack.genai_server.settings.settings import settings

        session = settings.DEFAULT_SESSION

    for component_name, component_config in config.get("components").items():
        cls = get_component_class(component_name, component_config.get("name"))
        configurations: dict = component_config.get("config")

        # Override config based on session
        if session:
            if (
                component_name == StackComponentType.VECTOR_DB.value
                or component_name == StackComponentType.MEMORY.value
            ):
                configurations["index_name"] = session.meta_data[component_name]["index_name"]
        if overide_config:
            if component_name in overide_config:
                configurations.update(overide_config[component_name])
        components[component_name] = cls.from_kwargs(**configurations)
    # To avoid circular import error
    from genai_stack.stack.stack import Stack

    stack = Stack(**components, run_etl=False)
    return stack
