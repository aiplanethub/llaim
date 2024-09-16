#!/usr/bin/env python

"""Tests for `genai_server`."""

import requests

from tests.api.test_genai_server import TestCaseServer


class TestSessionServerAPIs(TestCaseServer):

    def setUp(self) -> None:
        super().setUp()
        self.base_url = self.base_url + "session"

    def test_create_session(self):
        response = requests.post(url=self.base_url)
        assert response.status_code == 200

    def test_sessions_list(self):
        response = requests.get(url=self.base_url)
        assert response.status_code == 200

    def test_get_session(self):
        response = requests.get(
            url=self.base_url + "/1",
            params={"session_id": 1},
        )
        assert response.status_code == 200

    def test_delete_session(self):
        response = requests.delete(
            url=self.base_url + "/1",
            params={"session_id": 1},
        )
        assert response.status_code == 200
