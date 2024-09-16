#!/usr/bin/env python

"""Tests for `genai_server`."""

import requests

from tests.api.test_genai_server import TestCaseServer


class TestRetrieverServerAPIs(TestCaseServer):

    def setUp(self) -> None:
        super().setUp()
        self.base_url = self.base_url + "retriever"

    def test_retrieve(self):
        response = requests.get(
            url=self.base_url + "/retrieve",
            params={"session_id": 1, "query": "Where is sunil from ?"},
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        print(data)
        assert "output" in data.keys()
