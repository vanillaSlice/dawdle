from flask import url_for

from tests.utils import TestBlueprint


class TestHome(TestBlueprint):

    def test_index_GET_200(self):
        response = self.client.get(
            url_for("home.index_GET"),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Swagger UI" in response.data
