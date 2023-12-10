import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from server import app as flask_app, delete_test_user
import pytest


@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client
    


def test_signup(client):
    response = client.post('/signup', data={
        'username': 'newuser12',
        'email': 'newuser@example.com',
        'password': 'newpass12'
    })
    assert "/login" in response.headers["Location"]

def test_login(client):
    response = client.post('/login', data={
        'username': 'newuser12',
        'password': 'newpass12'
    })
    assert "/home" in response.headers["Location"]

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert "/login" in response.request.url
    delete_test_user("newuser12")

    

