from flask import url_for

from tests.test_base import TestBase


class TestHome(TestBase):

    #
    # index_GET tests.
    #

    def test_index_GET_not_authenticated(self):
        self.logout()
        self._assert_index_GET_response(200)

    def test_index_GET(self):
        self._assert_index_GET_response(302)

    def _assert_index_GET_response(self, status_code):
        response = self.client.get(url_for('home.index_GET'))
        assert response.status_code == status_code
