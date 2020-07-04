"""
all = open('data.txt') # megnyitja az állományt olvasásra alapértelmezetten

print(all) # output: <_io.TextIOWrapper name='data.txt' mode='r' encoding='cp1252'>

#############################

"""

nobel_winners = [
    {
        'category': 'Physics',
        'name': 'Albert Einstein',
        'nationality': 'Swiss',
        'sex': 'male',
        'year': 1921
    },
    {
        'category': 'Physics',
        'name': 'Paul Dirac',
        'nationality': 'British',
        'sex': 'male',
        'year': 1933
    },
    {
        'category': 'Chemistry',
        'name': 'Marie Curie',
        'nationality': 'Polish',
        'sex': 'female',
        'year': 1911
    }
]

##############################
"""

f = open('nobel_winners.csv', 'w')

print(f)

cols = list(nobel_winners[0].keys()) # lekéri a lista első dict objektumának kulcsait: category, name, nationality, sex, year, azért alakítom listává, hogy sortolható legyen
cols.sort() # rendezzük alfabetikusan

with open('nobel_winners.csv', 'w') as f: # a with arra jó, hogy garantálja, ha esetleg hiba történik a feldolgozás során az állomány bezáródik, ugyanez történik, ha kilépünk a blokkból
    f.write(','.join(cols) + '\n') # kiírjuk a kulcsokat az első sorba, vesszővel elválasztva

    for o in nobel_winners:
        row = [str(o[col]) for col in cols] # kiírjuk az adatokat a dict objektumokból
        f.write(','.join(row) + '\n')


with open('nobel_winners.csv', 'r') as f:
    [print(line, end='') for line in f.readlines()] # kiírjuk a terminálba a csv állományban található adatokat

###############################

import csv

with open('nobel_winners.csv', 'w') as f:
    field_names = list(nobel_winners[0].keys()) # a writer-nek explicit módon megkell mondanunk milyen mezőnevekkel dolgozunk, ebben az esetben a category, stb..
    field_names.sort()

    writer = csv.DictWriter(f, fieldnames=field_names) # a DictWriter alakítsa át a dict objektumokat csv sorokká
    writer.writeheader() # kiírjuk a mezőneveket a csv fájlba

    for w in nobel_winners:
        writer.writerow(w)

with open('nobel_winners.csv', 'r') as f:
    reader = csv.reader(f)

    for row in reader:
        print(row)

with open('nobel_winners.csv', 'r') as f:
    reader = csv.DictReader(f)

    nobel_winners = list(reader)
    
##############################

import json

with open('nobel_winners.json', 'w') as f:
    json.dump(nobel_winners, f) # egyszerűen létrehozza a fenti nobel_winners dict objektumokból álló listából a json állományt

with open('nobel_winners.json', 'r') as f:
    nobel_winners = json.load(f) # megnyitja és belemásolja a json állomány tartalmát a nobel_winners változóba

#############################


import datetime
from dateutil import parser
import json

class JSONDateTimeEncoder(json.JSONEncoder): # örökli az alapértelmezett JSON enkóder metódusait és tulajdonságait, ahhoz, hogy saját datetime-ra szakosodotatt készítsünk
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)): # lellenőrzi azt, hogy datetime típusú-e az objektum
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def dumps(obj):
    return json.dumps(obj, cls=JSONDateTimeEncoder) # használjuk a szerializációs metódust, beállítva a cls argumentummal a saját enkóderünket

now_str = dumps({'time': datetime.datetime.now()}) # átalakítja json formátumba a jelenlegi időt

time_str = '2020-07-08 14:22:15'

dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # a strptime megpróbálja megegyeztetni a date-stringet annak a formátumnak, amit második argumentumként megadunk, ha sikerül visszatéríti a datetime példányt"""

###############################

"""
from sqlalchemy import create_engine

engine = create_engine('sqlite:///nobel_prize.db', echo=True)
# Ebben az esetben az állomány-alapú SQLite adatbázist használjuk, az echo Igazra állításával azt érjük el, hogy az 
# SQLAlchemy-vel generált SQL instrukciók kiíródnak a terminálba

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base(bind=engine)

class Winner(Base):
    __tablename__ = 'winners' # elnevezi az SQL-táblát és ezt a kulcsszót használhatjuk annak eléréséhez

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    year = Column(Integer)
    nationality = Column(String)
    sex = Column(Enum('male', 'female'))
    # beállítottuk a tábla-sémáját, meghatározva a tábla oszlopok típusát

    def __repr__(self):
        return "<Winner(name={}, category={}, year={})>".format(self.name, self.category, self.year)
    # opcionális metódus, amelyet a tábla-sor kiírására fogjuk használni

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

albert = Winner(**nobel_winners[0])
# a Python ** operátorja kicsomagolja az első nober_winners elemet key-value párokként, tehát (name=Albert Einstein, category=Physics...)
session.add(albert)
session.new
# a new metódus segítségével beállítjuk az összes elemet, amelyet hozzáadtunk a session-höz.

session.expunge(albert)
# törli az argumentumként megadott példányt, akár az összeset is törölhetjük az expunge_all() metódussal
session.new

winner_rows = [Winner(**w) for w in nobel_winners]
# létrehoz egy listányi Winner példányt a nobel_winners elemeiből
session.add_all(winner_rows)
session.commit()
# beilleszti a session IdentitySet-jéből az összes elemet az adatbázisba
"""

"""result = session.query(Winner).filter_by(nationality='Swiss')
print(list(result))

res = session.query(Winner).order_by('year')
print(list(res))

#################################

def inst_to_dict(inst, delete_id=True):
    dat = {}

    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
        # eléri a példány tábla class-át, hogy megszerezze az oszlop objektumok listáját
        # egyszerűen elérjük annak a táblának az oszlopait, amelyhez tartozik a példány
        # a getattr() függvénnyel pedig megszerezzük annak a mezőnek az értékét
    if delete_id:
        dat.pop('id')
        # ha a delete_id igaz, akkor törölje az SQL elsődleges id mezőjét

    return dat

winner_rows = session.query(Winner)
nobel_winners = [inst_to_dict(w) for w in winner_rows]

###################################

marie = session.query(Winner).get(3)
marie.nationality = 'French'
session.dirty

session.commit()

session.query(Winner).get(3).nationality # 'French'

####################################

session.query(Winner).filter_by(name='Albert Einstein').delete()

list(session.query(Winner)) # Albert már nem jelenik meg"""

###################################

"""

import dataset

db = dataset.connect('sqlite:///nobel_prize.db') 
# csatlakozunk a már létező adatbázisunkhoz

wtable = db['winners']
winners = wtable.find()
winners = list(winners)
# lekértük az adatbázisban található összes sort, ami a winners táblán belül található

# töröljük a winners táblát
wtable = db['winners']
wtable.drop()

# majd újra létrehozzuk, és ekkor üres
wtable = db['winners']
list(wtable.find()) # output: []

with db as tx:
    # jelen esetben a with-re azért van szükség, hogy biztosan a tx tranzakció véglegesítésre kerüljön az adatbázisban
    for w in nobel_winners:
        tx['winners'].insert(w)

# ez után le is ellenőrízhetjük, hogy helyesen dolgoztunk-e

print(list(db['winners'].find()))

from datafreeze import freeze

winners = db['winners'].find()
freeze(winners, format='csv', filename='nobel_winners_ds.csv')

"""

#####################################

"""

from pymongo import MongoClient

client = MongoClient()
# létrehozza a Mongo-Client-et, felhasználva az alapértelmezett host-ot és port-okat
db = client.nobel_prize
# létrehozza és hozzafér a nobel_prize adatbázishoz
# a fenti utasítás esetében akár a client['nobel_prize'] forma is elfogadható, azonban úgy könnyebb hibázni
coll = db.winners
# ha a winners collection létezik, akkor lekéri, ha nem, akkor létrehozza

"""

"""

# alapértelmezett beállításokkal, csupán az adatbázisnév tetszőleges
def get_mongo_database(db_name, host='localhost', port=27017, username=None, password=None):
    # Elérjük a db_name-mel hivatkozott adatbázist MongoDB-ről, hitelesítő adatokkal vagy azok nélkül

    if username and password:
        mongo_uri = 'mongodb://{}:{}@{}/{}'.format(username, password, host, db_name)
        # URI = uniform resource identifier
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db_name] # itt már a második féle jelölést használjuk az adatbázis eléréséhez

db = get_mongo_database('nobel_prize')
coll = db['winners']
coll.insert_many(nobel_winners)
# beillesztjük az adatbázisba a dict objektumokat az insert metódussal
# ugyanakkor, ha kiírjuk a terminálba az eredeti listát, a nobel_winners-et, megfigyelhetjük
# hogy az insert metódus kiegészíti azt, hozzáad egy új 'id' mezőt.
# ezek ObjectId-k, amelyek későbbi lehívásokat tesznek lehetővé, de más egyéb rejtett funkcionalítással is rendelkeznek,
# mint pl. hogy rendelkeznek egy generálási idővel, amikoris az ObjectId létrejött

res = coll.find({'category': 'Chemistry'})
print(list(res))

res = coll.find({'year' : {'$gt': 1930}})
print(list(res))

def mongo_coll_to_dicts(dbname='test', collname='test', query={}, del_id=True, **kw):
    # a fenti paraméterlistában szereplő üres query, minden elemet lekér egy adott collection-ből
    db = get_mongo_database(dbname, **kw)
    res = list(db[collname].find(query))

    if del_id:
        for r in res:
            r.pop('_id')

    return res

print(mongo_coll_to_dicts('nobel_prize', 'winners'))

"""

"""

from datetime import datetime

d = datetime.now()
print(d.isoformat()) # output: 2020-07-04T19:13:47.622017

"""

from dateutil import parser

d = parser.parse('2020-07-04T16:13:47.622Z') # output: 2020-07-04 16:13:47.622000+00:00