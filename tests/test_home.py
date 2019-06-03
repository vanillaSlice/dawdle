from flask import url_for

from tests.test_base import TestBase

class TestHome(TestBase):

    def test_index_GET_not_authenticated(self):
        self.logout()
        response = self.client.get(url_for('home.index_GET'))
        assert response.status_code == 200

    def test_index_GET_authenticated(self):
        response = self.client.get(url_for('home.index_GET'))
        assert response.status_code == 302
