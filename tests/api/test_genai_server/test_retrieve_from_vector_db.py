#!/usr/bin/env python

"""Tests for `genai_server`."""
import json
import requests

from tests.api.test_genai_server import TestCaseServer


class TestRetrieverDataFromDBAPIs(TestCaseServer):

    def setUp(self) -> None:
        super().setUp()
        self.data = [
            {
                "id": self.create_session(),
                "document": [{
                    "page_content": "Cdjeus is a fruit and it is purple in color",
                    "metadata": {"source": "/path/1", "page": 1}
                }],
                "query": "What is the color of Cdjeus ?",
                "color": "purple"
            },
            {
                "id": self.create_session(),
                "document": [{
                    "page_content": "Dragorosour is an animal and it is green in color",
                    "metadata": {"source": "/path/2", "page": 2}
                }],
                "query": "What is the color of Dragorosour ?",
                "color": "green"
            },
            {
                "id": self.create_session(),
                "document": [{
                    "page_content": "Tektoplate is a planet and it is blue in color",
                    "metadata": {"source": "/path/3", "page": 3}
                }],
                "query": "What is the color of Tektoplate ?",
                "color": "blue"
            }
        ]

    def create_session(self):
        response = requests.post(url=self.base_url + "session")
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "id" in data.keys()
        return data.get("id")

    def add_document_to_session(self, session_id, data):
        response = requests.post(
            url=self.base_url + "vectordb/add-documents",
            data=json.dumps(
                {
                    "session_id": session_id,
                    "documents": data
                }
            ),
        )
        assert response.status_code == 200

    def search_for_doc(self, session_id, query):
        response = requests.get(
            url=self.base_url + "retriever/retrieve",
            params={"session_id": session_id, "query": query},
        )
        assert response.status_code == 200
        assert response.json()
        data = response.json()
        assert "output" in data.keys()
        return data.get("output")

    def test_search_vectordb_based_on_sessions(self):
        # Add documents to session
        for session in self.data:
            self.add_document_to_session(session.get("id"), session.get("document"))
        # assert color is present or not
        for session in self.data:
            for session_2 in self.data:
                if session.get("id") != session_2.get("id"):
                    output = self.search_for_doc(session.get("id"), session_2.get("query"))
                    print(f"{session.get('color')} not present in '{output}'")
                    assert session_2.get("color").lower() not in output.lower()
                else:
                    output = self.search_for_doc(session.get("id"), session_2.get("query"))
                    print(f"{session.get('color')} present in '{output}'")
                    assert session_2.get("color").lower() in output.lower()

