#!/usr/bin/env python

"""Tests for `genai_server`."""

import requests

from tests.api.test_genai_server import TestCaseServer


class TestETLServerAPIs(TestCaseServer):

    def setUp(self) -> None:
        super().setUp()
        self.base_url = self.base_url + "etl"

    def test_submit_job(self):
        response = requests.get(
            url=self.base_url + "/submit-job",
            params={"session_id": 1, "data": {"page_content": "Hello World", "metadata": {}}},
        )
        assert response.status_code == 200
        assert response.json().get("id") == 1
