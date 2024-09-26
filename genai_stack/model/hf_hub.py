from typing import Optional, Dict
from langchain.llms import HuggingFaceHub
from genai_stack.model.base import BaseModel, BaseModelConfig, BaseModelConfigModel


class HuggingFaceHubParameters(BaseModelConfigModel):
    """
    Data Model for the configs
    """
    repo_id: Optional[str] = "HuggingFaceH4/zephyr-7b-beta"
    """Model name to use."""
    model_kwargs: Optional[Dict] = None
    """Key word arguments passed to the model."""
    task: str = "text-generation"
    """Valid tasks: 'text2text-generation', 'text-generation', 'summarization'"""
    huggingface_api_token: str
    "HuggingFace Access Token"
    
class HuggingFaceHubConfigModel(BaseModelConfigModel):
    """
    Parameters for the configs
    """
    parameters: HuggingFaceHubParameters
    
class HuggingFaceHubConfig(BaseModelConfig):
    data_model = HuggingFaceHubConfigModel

class HuggingFaceHub(BaseModel):
    config_class = HuggingFaceHubConfig

    def _post_init(self, *args, **kwargs):
        self.model = self.load()

    def load(self):
        model = HuggingFaceHub.from_model_id(
            **self.config.parameters.dict()
        )
        return model

    def predict(self, prompt: str):
        response = self.model.predict(prompt)
        return {"output": response}
