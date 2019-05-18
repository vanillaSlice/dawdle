from tests.test_utils import TestBase

class TestHome(TestBase):

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200
