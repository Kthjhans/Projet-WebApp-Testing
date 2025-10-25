import os
import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

app = Flask(__name__)
app.secret_key = 'something_special'

def loadClubs():
    chemin = os.path.join(os.path.dirname(__file__), 'clubs.json')
    with open(chemin) as c:
        return json.load(c)['clubs']
    
def loadCompetitions():
    chemin = os.path.join(os.path.dirname(__file__), 'competitions.json')
    with open(chemin) as comps:
        return json.load(comps)['competitions']

clubs = loadClubs()
competitions = loadCompetitions()

# -------------------- ROUTES -------------------- #

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "supersecret"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash("Identifiants incorrects")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        flash("Veuillez vous connecter pour accéder à la page admin.")
        
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# @app.route('/showSummary', methods=['POST'])
# def showSummary():
#     club = next(c for c in clubs if c['email'] == request.form['email'])
#     return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((c for c in clubs if c['email'] == email), None)

    if club is None:
        flash("Email inconnu. Merci de vérifier votre saisie.")
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)



@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next(c for c in clubs if c['name'] == club)
    foundCompetition = next(c for c in competitions if c['name'] == competition)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    flash("Something went wrong-please try again")
    return render_template('admin.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next(c for c in competitions if c['name'] == request.form['competition'])
    club = next(c for c in clubs if c['name'] == request.form['club'])
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] -= placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

# -------------------- MAIN -------------------- #

if __name__ == '__main__':
    app.run(debug=True)
