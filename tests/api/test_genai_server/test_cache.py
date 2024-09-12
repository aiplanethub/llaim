#!/usr/bin/env python

"""Tests for `genai_server`."""
import unittest
import requests


class TestLLMCacheAPIs(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1:5000/api/llm-cache"

    def test_set_cache(self):
        response = requests.post(
            url=self.base_url + "/set-cache",
            json={
                "session_id": 1,
                "query": "Where is sunil from ?",
                "response": "Sunil is from Hyderabad.",
                "metadata": {"source": "/path", "page": 1}
            }
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "query" in data.keys()
        assert "metadata" in data.keys()
        assert "response" in data.keys()

    def test_get_cache(self):
        response = requests.get(
            url=self.base_url + "/get-cache",
            json={
                "session_id": 1,
                "query": "Where is sunil from ?"
            }
        )

        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "query" in data.keys()
        assert "metadata" in data.keys()
        assert "response" in data.keys()

    def test_get_and_set(self):
        query = "Where is sunil from ?"
        metadata = {"source": "/path", "page": 1}
        output = "Sunil is from Hyderabad."
        response = requests.post(
            url=self.base_url + "/set-cache",
            json={
                "session_id": 1,
                "query": query,
                "response": output,
                "metadata": metadata
            }
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "query" in data.keys() and data.get("query") == query
        assert "metadata" in data.keys() and data.get("metadata") == metadata
        assert "response" in data.keys() and data.get("response") == output

        response = requests.get(
            url=self.base_url + "/get-cache",
            json={
                "session_id": 1,
                "query": query
            }
        )

        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "query" in data.keys() and data.get("query") == query
        assert "response" in data.keys() and data.get("response") == output

        response = requests.get(
            url=self.base_url + "/get-cache",
            json={
                "session_id": 1,
                "query": "Where is sunil from ?",
                "metadata": {"source": "/pathdiff", "page": 1}
            }
        )
        assert response.status_code != 200

        response = requests.get(
            url=self.base_url + "/get-cache",
            json={
                "session_id": 1,
                "query": "Where is sunil from ?",
                "metadata": metadata
            }
        )

        assert response.status_code == 200
