import json
from unittest.mock import patch

from flask import url_for

from tests.components.contact.helpers import get_mock_contact_body
from tests.helpers import TestBase


class TestContact(TestBase):

    @patch("dawdle.components.contact.blueprints.send_contact_emails")
    def test_index_POST_204(self, send_contact_emails):
        body = get_mock_contact_body()
        response = self.__send_index_POST_request(body)
        self._assert_204(response)
        send_contact_emails.assert_called_with(
            body["email"],
            body["subject"],
            body["message"],
        )

    def test_index_POST_400_bad_data(self):
        body = get_mock_contact_body()
        del body["email"]
        response = self.__send_index_POST_request(body)
        self._assert_400(response, {
            "email": [
                "Missing data for required field.",
            ],
        })

    def test_index_POST_415(self):
        response = self._client.post(url_for("contact.index_POST"))
        self._assert_415(response)

    def __send_index_POST_request(self, body):
        return self._client.post(
            url_for("contact.index_POST"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )
