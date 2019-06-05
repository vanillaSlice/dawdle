from flask import url_for

from tests.test_base import TestBase

class TestContact(TestBase):

    def test_index_GET(self):
        response = self.client.get(url_for('contact.index_GET'))
        assert response.status_code == 200
