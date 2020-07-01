from dawdle import create_app


class TestBlueprint:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(testing=True)
        cls.app.app_context().push()
        cls.client = cls.app.test_client()
