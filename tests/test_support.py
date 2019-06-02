from tests.test_base import TestBase

class TestSupport(TestBase):

    def test_index(self):
        response = self.client.get('/support')
        assert response.status_code == 200
