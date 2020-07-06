from unittest.mock import patch

from flask import url_for

from tests.utils import TestBlueprint


class TestApp(TestBlueprint):

    @patch("dawdle.components.swagger.blueprints.send_from_directory")
    def test_500(self, send_from_directory):
        # do this temporarily to stop exceptions being thrown
        self.app.config.update({
            "DEBUG": False,
            "TESTING": False,
        })
        send_from_directory.side_effect = Exception()
        response = self.client.get(url_for("swagger_ui.template_GET"))
        self._assert_500(response)
