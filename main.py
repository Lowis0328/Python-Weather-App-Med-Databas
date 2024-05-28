from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import python_weather
import asyncio

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Konfigurera SQLAlchemy-delen av app-instansen
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

# Skapa SQLAlchemy db-instansen
db = SQLAlchemy(app)

def getEmoji(weatherKind):
    """
    Returnerar en emoji baserat på väderförhållandena.

    Parametrar:
    weatherKind (str): En sträng som representerar väderförhållandena.

    Returnerar:
    str: En emoji som representerar väderförhållandena.
    """
    if weatherKind == "Sunny":
     return "☀"
    elif weatherKind == "Cloudy":
        return "☁"
    elif weatherKind == "Rainy":
      return "🌧"
    elif weatherKind == "Snowy":
        return "❄"
    elif weatherKind == "Partly Cloudy":
        return "⛅"
    elif weatherKind == "Very Cloudy":
        return "☁"

class WeatherService:
    """
    En klass som används för att hämta väderinformation.

    Metoder:
    get_weather(self, city): Returnerar väderinformation för en specifik stad.
    """
    def __init__(self):
        pass

    async def get_weather(self, city):
        """
        Returnerar väderinformation för en specifik stad.

        Parametrar:
        city (str): Namnet på staden.

        Returnerar:
        dict: En dictionary med väderinformation.
        """
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)
            if weather:
                return weather
            else:
                print("Failed to retrieve weather info")

väderklass = WeatherService()

# Skapa din SQLALCHEMY databasmodell
class User(db.Model):
    """
    En klass som representerar en användare.

    Attribut:
    id (int): Användarens id.
    username (str): Användarens användarnamn.
    password (str): Användarens lösenord.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, password={self.password})'

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Hanterar inloggning av användare.

    Returnerar:
    str: Renderar en HTML-sida.
    """
    if request.method == 'POST':
        session.pop('user', None)

        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user'] = user.username
            return redirect(url_for('home'))

    print("Didnt find user in database")
    return render_template('login.html')

@app.route('/main')
def home():
    """
    Hanterar huvudsidan för inloggade användare.

    Returnerar:
    str: Renderar en HTML-sida.
    """
    if g.user:
        return render_template('index.html', user=session['user'])

    return redirect(url_for('login'))

@app.route('/Weather/<city>')
def WeatherInfo(city):
    """
    Hanterar väderinformation för en specifik stad.

    Parametrar:
    city (str): Namnet på staden.

    Returnerar:
    str: Renderar en HTML-sida.
    """
    if g.user:
        weather = asyncio.run(väderklass.get_weather(city))
        return render_template("weather.html", weather=weather, emoji=getEmoji(str(weather['kind'])))

    return redirect(url_for('login'))

@app.before_request
def before_request():
    """
    Kör innan varje begäran.

    Sätter g.user till användarnamnet i sessionen om det finns.
    """
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/dropsession')
def dropsession():
    """
    Tar bort användaren från sessionen.

    Returnerar:
    str: Renderar en HTML-sida.
    """
    session.pop('user', None)
    return render_template('login.html')

@app.route('/users')
def users():
    """
    Returnerar en lista över alla användare.

    Returnerar:
    str: En sträng med alla användare.
    """
    users = User.query.all()
    return '<br>'.join(str(user) for user in users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Hanterar registrering av användare.

    Returnerar:
    str: Renderar en HTML-sida eller en sträng med ett meddelande.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f"User {username} registered. Please <a href='/'>login</a>."
    else:
        return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)