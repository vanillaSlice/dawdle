from flask import url_for

from tests.helpers import TestBlueprint


class TestSwagger(TestBlueprint):

    def test_show_GET(self):
        response = self.client.get(
            url_for("swagger_ui.show"),
        )
        assert response.status_code == 200
        assert b"Swagger UI" in response.data

    def test_template_GET(self):
        response = self.client.get(
            url_for("swagger_ui.template_GET"),
        )
        assert response.status_code == 200
        assert b"Dawdle API" in response.data
