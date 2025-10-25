import pytest
import sys
import os

# === Correction pour pytest-xdist ===
# On ajoute la racine du projet au PYTHONPATH avant tout import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app  # ✅ maintenant Python peut le trouver


@pytest.fixture(scope="module")
def client():
    """
    Fixture Flask test client utilisée par tous les tests.
    (Arrange & Cleanup automatiques)
    """
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client  # <-- pytest fournit ce client à chaque test


# ✅ Exemple de tests basiques pour vérifier que tout fonctionne

def test_server_start_index(client):
    """Vérifie que la page d'accueil répond bien (Act + Assert)."""
    rv = client.get('/')
    assert rv.status_code == 200


def test_login_club(client):
    """Vérifie qu'un club peut se connecter (Act + Assert)."""
    rv = client.post('/showSummary', data={"email": "test1@irontemple.com"}, follow_redirects=True)
    assert rv.status_code == 200
    assert "Welcome, test1@irontemple.com" in rv.get_data(as_text=True)
