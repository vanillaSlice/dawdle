from flask import url_for

from tests.test_base import TestBase

class TestHome(TestBase):

    #
    # index_GET tests.
    #

    def assert_index_GET_response(self, status_code):
        response = self.client.get(url_for('home.index_GET'))
        assert response.status_code == status_code

    def test_index_GET_not_authenticated(self):
        self.logout()
        self.assert_index_GET_response(200)

    def test_index_GET(self):
        self.assert_index_GET_response(302)
