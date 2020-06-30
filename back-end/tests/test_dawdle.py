from flask import url_for

from dawdle import create_app


class TestHome:

    @classmethod
    def setup_class(cls):
        cls.app = create_app()
        cls.app.app_context().push()
        cls.client = cls.app.test_client()

    def test_index_GET_ok(self):
        response = self.client.get(
            url_for('home.index_GET'),
            follow_redirects=True,
        )
        assert response.status_code == 200
