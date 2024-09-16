#!/usr/bin/env python

"""Tests for `genai_server`."""

import unittest
import requests


class TestRetrieverServerAPIs(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1:5000/api/retriever"

    def test_retrieve(self):
        response = requests.get(
            url=self.base_url + "/retrieve",
            params={"session_id": 2, "query": "Where is sunil from ?"},
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        print(data)
        assert "output" in data.keys()
