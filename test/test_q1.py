import pytest
import sys
import os

# Permet de retrouver server.py depuis le dossier test/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client


#  Test : la page d'accueil fonctionne bien
def test_server_start_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    template = app.jinja_env.get_template('index.html')
    assert template.render().strip() in rv.get_data(as_text=True)


#  Test : connexion d’un club fonctionne bien
def test_login_club(client, email='test1@irontemple.com'):
    rv = client.post('/showSummary', data=dict(email=email), follow_redirects=True)
    assert rv.status_code == 200
    assert f"Welcome, {email}" in rv.get_data(as_text=True)


#  Test : vérifie que taper /admin sans être connecté redirige vers /login
def test_admin_redirects_to_login(client):
    rv = client.get('/admin', follow_redirects=False)
    assert rv.status_code in [302, 303]  # redirection
    assert '/login' in rv.headers['Location']  # redirige bien vers login


#  Test : vérifie que de mauvais identifiants ne permettent PAS d'accéder à /admin
def test_login_admin_with_invalid_credentials(client):
    rv = client.post('/login', data={'user_name': 'wrong', 'password': 'wrong'}, follow_redirects=True)
    assert rv.status_code == 200
    assert "Identifiants incorrects" in rv.get_data(as_text=True)
    rv_admin = client.get('/admin', follow_redirects=False)
    assert rv_admin.status_code in [302, 303]
    assert '/login' in rv_admin.headers['Location']


#  Test : vérifie que de bons identifiants permettent d’accéder à /admin
def test_login_admin_with_valid_credentials(client):
    rv = client.post('/login', data={'user_name': 'admin', 'password': 'supersecret'}, follow_redirects=True)
    assert rv.status_code == 200
    assert "Page Admin" in rv.get_data(as_text=True) or "Admin" in rv.get_data(as_text=True)


#  Test : vérifie que la déconnexion fonctionne et redirige vers /login
def test_logout(client):
    # Se connecter d’abord

    client.post('/login', data={'user_name': 'admin', 'password': 'supersecret'}, follow_redirects=True)
    # Puis se déconnecter

    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200
    assert b"login" in rv.data or b"Connexion" in rv.data # redirige bien vers la page de connexion
    


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client


#  Test paramétré pour plusieurs combinaisons de login admin
@pytest.mark.parametrize(
    "username,password,expected_status,expected_text",
    [
        # Cas valide — vérifie qu'on arrive bien sur la page admin
        ("admin", "supersecret", 200, "Admin Page"),
        
        # Cas invalides — on reste sur la page de connexion
        ("admin", "wrongpass", 200, "Page de connexion"),
        ("wronguser", "supersecret", 200, "Page de connexion"),
        ("", "", 200, "Page de connexion"),
    ],
)
def test_login_admin_parametrized(client, username, password, expected_status, expected_text):
    """
    Test paramétré qui vérifie différentes combinaisons de login admin.
    """
    rv = client.post('/login', data={
        'user_name': username,
        'password': password
    }, follow_redirects=True)

    # Vérifie le code de retour HTTP
    assert rv.status_code == expected_status

    # Vérifie que le texte attendu est bien dans la réponse
    html = rv.get_data(as_text=True)
    assert expected_text in html


#  TEST LOGIN PARAMÉTRÉ ADMIN


@pytest.mark.parametrize(
    "username,password,expected_text",
    [
        ("admin", "supersecret", "Admin Page"),  #  accès autorisé
        ("admin", "wrong", "Page de connexion"),
        ("wrong", "supersecret", "Page de connexion"),
        ("wrong", "wrong", "Page de connexion"),
    ]
)

def test_login_param(client, username, password, expected_text):
    """
    Test paramétré : vérifie que seule la combinaison correcte ('admin'/'admin')
    permet d'accéder à la page admin.
    """
    rv = client.post("/login", data={
        "user_name": username,
        "password": password
    }, follow_redirects=True)

    # On vérifie que le texte attendu est bien présent
    html = rv.get_data(as_text=True)
    assert expected_text in html

# ========================== TEST ACCÈS INTERDIT SANS CONNEXION ==========================

def test_access_welcome_without_email(client):
    """
    Vérifie qu'on ne peut pas accéder à la page welcome sans avoir soumis un email.
    """
    rv = client.post('/showSummary', data={"email": ""}, follow_redirects=True)

    assert rv.status_code == 200
    html = rv.get_data(as_text=True)

    #  Vérifie qu'on ne voit pas le message de bienvenue personnalisé
    assert "Welcome," not in html  
    #  Vérifie qu'on est bien resté sur la page d'accueil
    assert "Welcome to the GUDLFT Registration Portal!" in html

