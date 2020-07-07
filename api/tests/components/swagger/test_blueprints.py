from flask import url_for

from tests.helpers import TestBase


class TestSwagger(TestBase):

    def test_show_200(self):
        response = self.client.get(url_for("swagger_ui.show"))
        assert response.status_code == 200
        assert b"Swagger UI" in response.data

    def test_template_GET_200(self):
        response = self.client.get(url_for("swagger_ui.template_GET"))
        assert response.status_code == 200
        assert b"Dawdle API" in response.data
