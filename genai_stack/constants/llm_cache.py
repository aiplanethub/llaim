LLM_CACHE_MODULE = "genai_stack.llm_cache"
LLM_CACHE_CONFIG_KEY = "llm_cache"


class LLM_Cache:
    LANGCHAIN = "cache"


AVAILABLE_LLM_CACHE_MAPS = {
    LLM_Cache.LANGCHAIN:"cache/LLMCache",
}
