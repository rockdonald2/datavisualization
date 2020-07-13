""" from flask import Flask

app = Flask(__name__)

# a Flask route-ok lehetőséget nyújtanak arra, hogy irányítsuk a webes forgalmunkat, ez a root route, jelenleg a http://localhost:8000
@app.route('/')
def hello():
    return 'Hello World!'

# beállítja a port-ot, amelyen a lokális szerverünk futni fog,
# a debug módban pedig a Flask hasznos logokat fog kiírni a képernyőre, és error esetén egy böngésző-alapú jelentést fog adni
if __name__ == "__main__":
    app.run(port=8000, debug=True) """


# RESTful API w/ noSQL
""" from flask import Flask, request, abort
from pymongo import MongoClient
from bson.json_util import dumps, default

app = Flask(__name__)

db = MongoClient().nobel_prize

@app.route('/api/winners')

def get_country_data():
    query_dict = {}

    for key in ['country', 'category', 'year']:
        # a lenti metódus elréhetővé teszi számunkra a lekérdezés argumentumjait
        # amely valahogy így néz ki: '?country=Australia&category=Chemistry'
        arg = request.args.get(key)

        # majd a lekérdezés argumentumjai szerint összeállítjuk az API hívás lekérdezését
        if arg:
            query_dict[key] = arg

    # lehívjuk az adatbázisból a lekérdezés elemeit
    winners = db.winners_cleaned.find(query_dict)

    # ha sikerült
    if winners:
        # a dumps metódus nem úgy, mint a json.dumps metódus, képes szerializálni még dátum objektumokat is JSON-ná.
        # a szerializálás mégegyszer az a folyamat, amely során a komplex adatszerkezeteket byte streammé alakítjuk
        return dumps(winners)

    # ha nem sikerült leállítjuk 404-es státuszkóddal
    abort(404)

if __name__ == '__main__':
    app.run(port=8000, debug=True) """

# RESTful API w/ SQL
from flask import Flask, request, abort
import dataset
from bson.json_util import dumps, default

app = Flask(__name__)

db = dataset.connect('mysql+pymysql://root@localhost/nobel_prize')

@app.route('/api/winners')
def get_country_data():
    print('Request args: {}'.format(str(dict(request.args))))

    query_dict = {}

    for key in ['country', 'category', 'year']:
        arg = request.args.get(key)

        if arg:
            query_dict[key] = arg

    winners = db['winners_cleaned'].find(**query_dict)

    if winners:
        return dumps(winners)

    abort(404)

if __name__ == '__main__':
    app.run(port=8000, debug=True)