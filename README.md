### Introduktion

Detta projekt är en sammansatt webapplikation som kombinerar funktionalitet från både webbserverprogrammering och allmän programmering. Applikationen är byggd med Flask och inkluderar användarhantering, väderinformation från en tredjeparts-API och grundläggande sessionhantering samt object orienterad programmering.

### Funktionalitet

    Användarhantering: Registrering, inloggning och sessionhantering.
    Väderinformation: Hämtar väderinformation för en specifik stad med hjälp av python_weather.
    Rutter: Olika rutter för att hantera inloggning, väderfrågor och användarhantering.

# Teknologier

    Flask: Ett lättviktigt ramverk för webbapplikationer i Python.
    Flask-SQLAlchemy: ORM (Object Relational Mapper) för att interagera med databasen.
    SQLite: En lättviktig databas för att spara användarinformation.
    python_weather: Ett bibliotek för att hämta väderinformation.

# Installation

För att köra denna applikation lokalt, följ dessa steg:

1. Klona detta repo till din lokala maskin med `git clone https://github.com/Lowis0328/Python-Weather-App-Med-Databas.git`.
2. Installera de nödvändiga paketen med `pip install -r requirements.txt`.
3. Kör applikationen med `python main.py`.

   
# Användning

När applikationen körs kan du navigera till http://127.0.0.1:5000/ i din webbläsare. Här är en översikt över tillgängliga rutter:

    / Inloggningssida.
    /register: Registreringssida.
    /main: Huvudsida för inloggade användare.
    /Weather/<city>: Visar väderinformation för en specifik stad.
    /dropsession: Loggar ut användaren och rensar sessionen.
    /admin: Visar alla användare (endast för debug-syften).


# Filstruktur

```
weather_app/
├── app.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── weather.html
├── static/
├── test.db
├── requirements.txt
└── README.md
```


# Kodöversikt app.py

Huvudfilen för din applikation innehåller följande nyckelfunktioner:

### Database Configuration:

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

### User Model:

```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
```
### Routes:

  Login:
```
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user'] = user.username
            return redirect(url_for('home'))
    return render_template('login.html')
```
Register:
```

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} registered. Please <a href='/'>login</a>."
        return render_template("register.html")
```
### Weather Service:
```
class WeatherService:
    async def get_weather(self, city):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)
            return weather if weather else None
```


# Licens

Detta projekt är licensierat under MIT-licensen. Se LICENSE för mer information.

# Kontakt

För frågor eller support, vänligen kontakta [Lowe Granegärd].
