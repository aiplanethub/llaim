#!/usr/bin/env python

"""Tests for `genai_stack` package."""


import unittest

from genai_stack.embedding.langchain import LangchainEmbedding


class TestEmbedding(unittest.TestCase):
    def test_huggingface_embedding(self):
        config = {
            "model_name": "sentence-transformers/all-mpnet-base-v2",
            "model_kwargs": {"device": "cpu"},
            "encode_kwargs": {"normalize_embeddings": False},
        }
        embedding = LangchainEmbedding.from_kwargs(name="HuggingFaceEmbeddings", fields=config)
        embedding.load()
        embedding.embed_text("something")
