#!/usr/bin/env python

"""Tests for `genai_server`."""
import json
import unittest
import requests


class TestPromptEngineAPIs(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1:5000/api/prompt-engine/prompt"

    def test_get_prompt(self):
        response = requests.get(
            self.base_url,
            data=json.dumps({
                "session_id": 2,
                "type": "CONTEXTUAL_CHAT_PROMPT",
                "query": "What is the color of Cdjeus ?"
            })
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "CONTEXTUAL_CHAT_PROMPT"
        assert "template" in data.keys()

    def test_set_prompt(self):
        response = requests.post(
            self.base_url,
            data=json.dumps({
                "session_id": 2,
                "type": "CONTEXTUAL_QA_PROMPT",
                "template": "\nUse th3 backticks at the end. If you don\'t know the answer, just say that you don\'t know, don\'t try to make up an answer.\nPlease provide an answer which is factually correct and based on the information retrieved from the vector store.\nPlease also mention any quotes supporting the answer if any present in the context supplied within two double quotes "" .\n{context}\n\nQUESTION:```{query}```\nANSWER:\n"
            })
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "CONTEXTUAL_QA_PROMPT"
        assert "template" in data.keys()

    def test_get_and_set_prompt(self):
        template = "\nThe following is a conversation between an AI and Boy. If you don't know the answer, just say that you don't know,\ndon't try to make up an answer.\n\nCURRENT CONVERSATIONS:\n{history}\nHUMAN: {query}\nYOU:\n"
        response = requests.post(
            self.base_url,
            data=json.dumps({
                "session_id": 2,
                "type": "SIMPLE_CHAT_PROMPT",
                "template": template
            })
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "SIMPLE_CHAT_PROMPT"
        assert "template" in data.keys()
        assert data["template"] == template

        response = requests.get(
            self.base_url,
            data=json.dumps({
                "session_id": 2,
                "type": "SIMPLE_CHAT_PROMPT",
                "query": "What is the color of Cdjeus ?"
            })
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "SIMPLE_CHAT_PROMPT"
        assert "template" in data.keys()
        assert data["template"] == template

