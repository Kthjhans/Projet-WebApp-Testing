# Projet-WebApp-Testing
Ce projet contient les tests pour la webapp SpaceGame : - Tests unitaires avec `pytest` - Tests fonctionnels/UI avec Selenium
README.md (bref et clair)

## Description
Cette application est un site web de test (`SpaceGame`).  
Elle inclut des fonctionnalités de login, tableau de scores et fenêtres modales pour les joueurs.  
Le dépôt contient des tests **unitaires Flask** et des **tests fonctionnels Selenium** pour vérifier le comportement sur Chrome, Firefox et Edge.

## Installation
```bash
git clone https://github.com/Kthjhans/Projet-WebApp-Testing.git
cd Projet-WebApp-Testing
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

Lancer l'application
python server.py


Le site sera disponible sur http://127.0.0.1:5000.

Exécuter les tests
Tests unitaires Flask
pytest -n 4

Tests fonctionnels Selenium (multi-browser)
pytest -n 3 selenium_tests/ --html=selenium_report.html
