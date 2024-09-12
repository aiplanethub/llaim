from typing import Any, Dict, List, Optional
from langchain.llms.vllm import VLLM as Vllm
from pydantic import Field

from genai_stack.model.base import BaseModelConfigModel, BaseModelConfig, BaseModel

class VLLMParameters(BaseModelConfigModel):
    """VLLM language model."""

    model: str = ""
    """The name or path of a HuggingFace Transformers model."""

    temperature: float = 1.0
    """Float that controls the randomness of the sampling."""

    max_new_tokens: int = 512
    """Maximum number of tokens to generate per output sequence."""

    top_k: int = 4
    """Integer that controls the number of top tokens to consider."""

    top_p: float = 1.0
    """Float that controls the cumulative probability of the top tokens to consider."""

    n: int = 1
    """Number of output sequences to return for the given prompt."""

    dtype: str = "auto"
    """The data type for the model weights and activations."""

    download_dir: Optional[str] = None
    """Directory to download and load the weights. (Default to the default 
    cache dir of huggingface)"""

    vllm_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `vllm.LLM` call not explicitly specified."""

    tensor_parallel_size: Optional[int] = 1
    """The number of GPUs to use for distributed execution with tensor parallelism."""

    trust_remote_code: Optional[bool] = False
    """Trust remote code (e.g., from HuggingFace) when downloading the model 
    and tokenizer."""

    best_of: Optional[int] = None
    """Number of output sequences that are generated from the prompt."""

    presence_penalty: float = 0.0
    """Float that penalizes new tokens based on whether they appear in the 
    generated text so far"""

    frequency_penalty: float = 0.0
    """Float that penalizes new tokens based on their frequency in the 
    generated text so far"""

    use_beam_search: bool = False
    """Whether to use beam search instead of sampling."""

    stop: Optional[List[str]] = None
    """List of strings that stop the generation when they are generated."""

    ignore_eos: bool = False
    """Whether to ignore the EOS token and continue generating tokens after 
    the EOS token is generated."""

    logprobs: Optional[int] = None
    """Number of log probabilities to return per output token."""

class VLLMConfigModel(BaseModelConfigModel):
    parameters:VLLMParameters

class VLLMConfig(BaseModelConfig):
    data_model = VLLMConfigModel

class VLLM(BaseModel):
    config_class = VLLMConfig

    def _post_init(self, *args, **kwargs):
        self.model = self.load()

    def load(self):
        """
        Using dict method here to dynamically access object attributes
        """
        model = Vllm(**self.config.parameters.dict())
        return model

    def predict(self, prompt: str):
        response = self.model.predict(prompt)
        return {"output": response}