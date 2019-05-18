from dawdle import create_app

class TestBase:

    def setup_method(self):
        # set up test app instance
        self.app = create_app(testing=True)
        self.app.app_context().push()
        self.client = self.app.test_client()
