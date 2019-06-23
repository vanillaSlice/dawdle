from flask import url_for

from tests.test_base import TestBase


class TestHome(TestBase):

    #
    # index_GET tests.
    #

    def test_index_GET_not_authenticated(self):
        self.logout()
        self._assert_index_GET_ok(b'Welcome to Dawdle!')

    def test_index_GET(self):
        self._assert_index_GET_ok(b'Personal Boards')

    def _assert_index_GET_ok(self, text):
        response = self.client.get(
            url_for('home.index_GET'),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert text in response.data
