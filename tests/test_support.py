from flask import url_for

from tests.test_base import TestBase

class TestSupport(TestBase):

    def test_index_GET(self):
        response = self.client.get(url_for('support.index_GET'))
        assert response.status_code == 200
