# test/test_admin_auth.py
import pytest
from server import app, ADMIN_USERNAME, ADMIN_PASSWORD

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client

# def test_admin_redirect_to_login(client):
#     # accès direct à /admin sans session
#     rv = client.get('/admin', follow_redirects=True)
#     assert rv.status_code == 200
#     assert b"Bienvenue sur la page Admin" in rv.data

def test_admin_login_invalid_credentials(client):
    rv = client.post('/login', data={"user_name": "wrong", "password": "wrong"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Identifiants incorrects" in rv.data

def test_admin_login_valid_credentials(client):
    rv = client.post('/login', data={"user_name": ADMIN_USERNAME, "password": ADMIN_PASSWORD}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Admin Page" in rv.data or b"Bienvenue administrateur" in rv.data
