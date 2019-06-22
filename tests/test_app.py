from tests.test_base import TestBase


class TestApp(TestBase):

    def test_404(self):
        response = self.client.get('/this/page/does/not/exist')
        assert response.status_code == 404
