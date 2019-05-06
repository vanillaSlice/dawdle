import pytest

from dawdle import create_app

client = create_app().test_client()

def test_home():
    res = client.get('/')
    assert res.status_code == 200
