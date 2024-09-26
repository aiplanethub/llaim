from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoTokenizer
import torch

from genai_stack.fine_tune.base import BaseFineTune, BaseFineTuneConfigModel
import ray


class LLama27bConfigModel(BaseFineTuneConfigModel):
    model_name: str = "daryl149/llama-2-7b-chat-hf"
    dataset: str


class LLama27bFineTune(BaseFineTune):
    config_class = LLama27bConfigModel

    def load_model(self, model_name: str):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        torch.cuda.get_device_capability()
        device_map = "auto"

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map=device_map,
        )
        model.config.pretraining_tp = 1

        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, use_fast=True)
        tokenizer.pad_token = tokenizer
        torch.cuda.empty_cache()
        print("model", model)
        print("tokenizer", tokenizer)
        return model, tokenizer

    def load_dataset(self):
        datasets = load_dataset(self.config.dataset)
        ray_datasets = {
            "train": ray.data.from_huggingface(datasets["train"]),
            "validation": ray.data.from_huggingface(datasets["validation"]),
            "test": ray.data.from_huggingface(datasets["test"]),
        }
        return ray_datasets
