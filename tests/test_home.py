from tests.test_base import TestBase

class TestHome(TestBase):

    def test_404(self):
        response = self.client.get('/this/page/does/not/exist')
        assert response.status_code == 404

    def test_index_not_authenticated(self):
        self.logout()
        response = self.client.get('/')
        assert response.status_code == 200

    def test_index_authenticated(self):
        response = self.client.get('/')
        assert response.status_code == 302
