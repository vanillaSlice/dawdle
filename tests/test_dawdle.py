import pytest

from dawdle import create_app

@pytest.fixture
def app():
    yield create_app(testing=True)

@pytest.fixture
def client(app):
    yield app.test_client()

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
