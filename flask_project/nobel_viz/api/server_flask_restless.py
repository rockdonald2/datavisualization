# server_flask_restless.py

import flask
import flask_sqlalchemy
import flask_restless
from flask_cors import CORS

# létrehozzuk a Flask applikációt és a Flask-SQLAlchemy objektumot
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/nobel_prize'

app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

db = flask_sqlalchemy.SQLAlchemy(app)


# ezután létrehozzuk a Flask-SQLAlchemy modelleket, a megszokott módon,
# de két fontos resztrikcióval:
#   1. Muszáj legyen ezeknek a modelleknek egy primary key oszlopja, vagy sqlalchemy.Integer vagy sqlalchemy.Unicode típusból
#   2. Muszáj legyen egy __init__ metódusuk, amely az összes oszlopra fogad el kulcsszó argumentumokat
# a 2. esetében elmondható, hogy a flask.ext.sqlalchemy.SQLAlchemy.Model biztosít egy ilyen __init__ metódust,
# tehát nem kell újat létrehozzunk jelenesetben

# alapértelmezetten a lenti modell neve a tábla neve kell legyen,
# de ezt expliciten a lenti változóval is képesek vagyunk meghatározni
class Winners(db.Model):
    __tablename__ = 'winners_cleaned_w_bios'

    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    category = db.Column(db.Unicode)
    year = db.Column(db.Unicode)
    country = db.Column(db.Unicode)
    gender = db.Column(db.Unicode)
    award_age = db.Column(db.Integer)

# létrehozza az adatbázis táblákat
db.create_all()

# létrehozzunk egy Flask-Restless API managert
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# létrehozzuk az API endpointokat, amelyek elérhetők lesznek az /api/<táblanév>-en alapértelmezetten
# meghatározhatjuk a HTTP metódusokat is, amelyek elérhetők lesznek
# a collection_name-el meglehet határozni az endpointokat, amelyen keresztül elérhető lesz az API
manager.create_api(Winners, collection_name='winners', methods=['GET'], max_results_per_page=1000)

cors = CORS(app)

# elindítjuk a Flask loopot
app.run()