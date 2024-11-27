#!/usr/bin/env python

"""Tests for `genai_server`."""
import unittest
import requests


class TestEmbeddingServerAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1:5000/api/embedding"

    def test_embed_test(self):
        response = requests.post(
            url=self.base_url + "/embed-text",
            json={
                "text": "New Delhi is the capital of India.",
                "session_id": 1
            }
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "embedding" in data
        assert type(data["embedding"]) == list
