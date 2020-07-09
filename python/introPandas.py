import pandas as pd

''' # a függvény visszatérít egy DataFrame-t, elemezve a megadott JSON fájlt
# konvenció szerint a DataFrame változók df-el kezdődnek
df = pd.read_json('nobel_winners.json')

print(df.head()) '''

# output:
#     category             name nationality     sex  year
# 0    Physics  Albert Einstein       Swiss    male  1921
# 1    Physics       Paul Dirac     British    male  1933
# 2  Chemistry      Marie Curie      Polish  female  1911

''' df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/minibios.json')

print(df.head()) '''

df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')

''' print(df.head())

print(df.columns)
# output: Index(['link', 'name', 'year', 'category', 'country', 'born_in', 'text'], dtype='object')

print(df.index)
# output: RangeIndex(start=0, stop=1163, step=1)

# használjuk a set_index metódust, hogy beállítsuk a DataFrame indexét a 'name' oszlopra,
df = df.set_index('name')
# majd használjuk a loc metódust, hogy kiválasszunk sorokat, amelyek tartalmazzák a megadott elemet
print(df.loc['Albert Einstein'])
# végül, használva a reset_index metódust visszaállítjuk az eredeti állapotába
df = df.reset_index()

# kiválasztja a metódus a második sort
print(df.iloc[2]) '''

''' name_col = df.name # == df['name']
print(type(name_col))
print(name_col) '''

''' <class 'pandas.core.series.Series'>
0                            Howard Florey
1              Sir Frank Macfarlane Burnet
2                   William Lawrence Bragg
3                         César Milstein *
4                        John Carew Eccles
                       ...
1158                         Albert Claude
1159    International Atomic Energy Agency
1160                          Peter Handke
1161                     Corneille Heymans
1162                      Elfriede Jelinek
Name: name, Length: 1163, dtype: object '''

''' # kiválasztjuk a kategória oszlopot
df = df.groupby('category')
print(df.groups.keys())
# output: dict_keys(['', 'Chemistry', 'Economics', 'Literature', 'Peace', 'Physics', 'Physiology or Medicine'])
# azért van egy üres kategória is, mert elírták a Wikipédia oldalon, és nem egységes a jelölés

# lekérjük, majd kiírjuk a fizikai Nobel-díj győzteseket
phy_group = df.get_group('Physics')
print(phy_group.head()) '''

''' print(df.category == 'Physics') '''

''' output: 
0       False
1       False
2        True
3       False
4       False
        ...
1158    False
1159    False
1160    False
1161    False
1162    False '''

''' print(df[df.category == 'Physics']) '''

''' output:
                                                   link  ...                                               text
2     http://en.wikipedia.org/wiki/William_Lawrence_...  ...             William Lawrence Bragg , Physics, 1915
6            http://en.wikipedia.org/wiki/Brian_Schmidt  ...  Brian Schmidt ,  born in the United States , P...
17    http://en.wikipedia.org/wiki/Erwin_Schr%C3%B6d...  ...                  Erwin Schrödinger , Physics, 1933
18     http://en.wikipedia.org/wiki/Victor_Francis_Hess  ...                Victor Francis Hess , Physics, 1936
27          http://en.wikipedia.org/wiki/Wolfgang_Pauli  ...                     Wolfgang Pauli , Physics, 1945
...                                                 ...  ...                                                ...
1131         http://en.wikipedia.org/wiki/Brian_Schmidt  ...  Brian Schmidt ,  born in the United States , P...
1147      http://en.wikipedia.org/wiki/Donna_Strickland  ...                   Donna Strickland , Physics, 2018
1149  http://en.wikipedia.org/wiki/William_Lawrence_...  ...             William Lawrence Bragg , Physics, 1915
1151    http://en.wikipedia.org/wiki/Arthur_B._McDonald  ...                 Arthur B. McDonald , Physics, 2015
1156  http://en.wikipedia.org/wiki/Fran%C3%A7ois_Eng...  ...                   François Englert , Physics, 2013 '''

''' df = pd.DataFrame({
    'name': ['Albert Einstein', 'Marie Curie', 'William Faulkner'],
    'category': ['Physics', 'Chemistry', 'Literature']
})

print(df.head()) '''
''' output:
               name    category
0   Albert Einstein     Physics
1       Marie Curie   Chemistry
2  William Faulkner  Literature '''

''' df = pd.DataFrame.from_dict([
    {'name': 'Albert Einstein', 'category': 'Physics'},
    {'name': 'Marie Curie', 'category': 'Chemistry'},
    {'name': 'William Faulkner', 'category': 'Literature'}
])

print(df.head()) '''
''' output:
               name    category
0   Albert Einstein     Physics
1       Marie Curie   Chemistry
2  William Faulkner  Literature '''

''' df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')

# elvégezzük a szükséges műveletek a df-en ...

json = df.to_json('./nobel_prize/nobel_winners/nobel_winners/nwinners_cleaned.json', orient='records') '''

''' 
df = pd.read_csv('nobel_winners.csv') '''

''' from io import StringIO

data = " `Albert Einstein`| Physics \n`Marie Curie`| Chemistry"

# meghatározzuk a szokásostól eltérő jelöléseket, mint a mező elválasztó |-t, a kategóriák neveit, 
# a kezdeti space kihagyását, és azt a jelölési módot, ahogy a szóközt tartalmazó stringek vannak jelölve
df = pd.read_csv(StringIO(data), sep='|', names=['name', 'category'], skipinitialspace=True, quotechar="`")

print(df.head()) '''
''' output:
              name   category
0  Albert Einstein   Physics
1      Marie Curie  Chemistry '''

''' csv = df.to_csv('data.csv', encoding='utf-8') '''

''' dfs = {}
xls = pd.ExcelFile('nobel_winners.xlsx') # betölti az Excel fájlt
# fogja a munkalapot név szerint, és lementi egy dict-be
dfs['WSheet1'] = xls.parse('WinnersSheet1', na_values = ['NA'])
# ugyanúgy, azonban ebben az esetben meghatározzuk előszöris az oszlopot, pozíció szerint, hogy használjuk, mint a DataFrame sorcímkéi
# az na_values esetében meghatározzuk azon stringeket, amelyeket NaN-ként kell értelmezzen
# végül a skiprows esetében a sorok számát határozzuk meg, amelyeket kikell hagyjon feldolgozás előtt, pl. metaadat lenne ezekben
dfs['WSheet2'] = xls.parse('WinnersSheet2', index_col=0, na_values=['-'], skiprows=3) '''

''' # ebben az esetben a második munkalap rosszul formázottsága miatt nem megfelelően olvassa be
data = pd.read_excel('nobel_winners.xlsx', ['WinnersSheet1', 'WinnersSheet2'], index_col=None, na_values = ['NA']) '''

''' data = pd.read_excel('nobel_winners.xlsx')

data = pd.read_excel('nobel_winners.xlsx', None) '''

''' data = pd.read_excel('nobel_winners.xlsx', 'WinnersSheet1', index_col=0, usecols='A:C') '''

''' df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')

# lementi a DataFrame értékeit a nobel_winners Excel fájlba, létrehozva egy új munkalapot WinnersSheet3 néven
# fontos megjegyezni azt, hogy teljesen új Excel fájlt hoz létre, törölve a már létező munkalapokat
excel = df.to_excel('nobel_winners.xlsx', sheet_name='WinnersSheet3') '''

''' df1 = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')
df2 = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/minibios.json')

# ebben az esetben mindkét DataFrame-t ugyanabba az Excel fájlba fogja írni
with pd.ExcelWriter('nobel_winners.xlsx') as writer:
    df1.to_excel(writer, sheet_name='WinnersSheet')
    df2.to_excel(writer, sheet_name='WinnersBios') '''

''' # emellett szükség volt a pymysql módul telepítésére is pip-el
import sqlalchemy

# előszöris, létrehozzuk a tárolómotrot, megadva az adatbázis elérését, illetőleg annak nevét
engine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/nobel_prize') '''

''' # megadjuk első argumentumként a beolvasandó SQL tábla nevét, majd a tárolómotrot
df = pd.read_sql('nobel_winners', engine) '''

''' # beolvassuk a JSON állományt, amelyet kiszeretnénk írni
df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')
# kiírjuk az adatbázisba, az első argumentumban meghatározva az SQL tábla nevét, 
# megadva a tárolómotrot, illetőleg 500-as chunkokban, sorokban, fogja kiírni
df.to_sql('nobel_winners', engine, chunksize=500) '''

''' from sqlalchemy.types import String

df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')
# mivel a VARCHAR típust használja, ezért megkell adni a hosszt is
df.to_sql('nobel_winners', engine, dtype={'year': String(4)}) '''

''' from pymongo import MongoClient

# létrehozunk egy Mongo klienst, az alapértelmezetten host-al és port-al
client = MongoClient() '''

''' # lekérjük a nobel_prize adatbázist
db = client.nobel_prize
# megkeresi az összes dokumentumot a winners collection-ön belül
cursor = db.winners.find()
# beolvassa az összes dokumentumot a winners collection-ön belül listaként, hogy létrehozza a DataFrame-t
df = pd.DataFrame(list(cursor)) '''

''' # alapértelmezett beállításokkal, csupán az adatbázisnév tetszőleges
def get_mongo_database(db_name, host='localhost', port=27017, username=None, password=None):
    """ Elérjük a db_name-mel hivatkozott adatbázist MongoDB-ről, hitelesítő adatokkal vagy azok nélkül """

    if username and password:
        mongo_uri = 'mongodb://{}:{}@{}/{}'.format(username, password, host, db_name)
        # URI = uniform resource identifier
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db_name] # itt már a második féle jelölést használjuk az adatbázis eléréséhez

# felhasználva a korábban létrehozott függvényünket elérjük az adatbázist

db = get_mongo_database('nobel_prize')

df = pd.read_json('./nobel_prize/nobel_winners/nobel_winners/nwinners.json')
records = df.to_dict(orient='records')
db['nwinners_full'].insert_many(records)

def mongo_to_dataframe(db_name, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Létrehoz egy DataFrame-t egy MongoDB collection-ból """

    db = get_mongo_database(db_name, host, port, username, password)

    # megkeresi a collection-ból a lekérdezés szerinti elemeket
    cursor = db[collection].find(query)

    df = pd.DataFrame(list(cursor))

    # amennyiben azt szeretnénk, hogy törölje ki a MongoDB által hozzáadott id-t
    if no_id:
        del df['_id']

    return df

def dataframe_to_mongo(df, db_name, collection, host='localhost', port=27017, username=None, password=None):
    """ Lement egy DataFrame-t egy MongoDB collection-be """

    db = get_mongo_database(db_name, host, port, username, password)

    records = df.to_dict(orient='records')

    db[collection].insert_many(records) '''
    
''' import numpy as np

s = pd.Series(np.arange(1, 5)) # == pd.Series([1, 2, 3, 4])
print(s) '''

''' output:
0    1  # index, value
1    2
2    3
3    4
dtype: int32 '''

''' s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
print(s) '''

''' output:
a    1
b    2
c    3
d    4
dtype: int64 '''

''' s = pd.Series({'a': 1, 'b': 2, 'c':3, 'd':4 })
print(s) '''

''' output:
a    1
b    2
c    3
d    4
dtype: int64 '''

''' s = pd.Series({'a': 1, 'b': 2, 'd': 4}, index=['a', 'b', 'c'])
print(s) '''

''' output:
a    1.0
b    2.0
c    NaN
dtype: float64 '''

''' s = pd.Series(9, index=[1, 2, 3])
print(s) '''

''' output:
1    9
2    9
3    9
dtype: int64 '''

''' import numpy as np

s = pd.Series(np.arange(1, 5), index=['a', 'b', 'c', 'd'])
s = np.sqrt(s)
print(s) '''

''' output:
a    1.000000
b    1.414214
c    1.732051
d    2.000000
dtype: float64 '''

''' print(s[1:3]) '''

''' output:
b    1.414214
c    1.732051
dtype: float64 '''

''' print(pd.Series([6, 3.2, 'foo']) + pd.Series([3, 0.8, 'bar'])) '''

''' output:
0         9
1         4
2    foobar
dtype: object '''

''' # a name argumentummal egyszerűen meghatározok a Series nevét, amely később az oszlopnév lesz
names = pd.Series(['Albert Einstein', 'Marie Curie'], name='name')
categories = pd.Series(['Physics', 'Chemistry'], name='category')

# az axis=1 által "vízszintesre" állítjuk az összesítést, azaz azt határozzuk meg, hogy a Series-ek oszlopok
df = pd.concat([names, categories], axis=1)
print(df.head()) '''

''' output:
              name   category
0  Albert Einstein    Physics
1      Marie Curie  Chemistry '''

df1 = pd.DataFrame({'foo': [1, 2, 3], 'bar': ['a', 'b', 'c']})
df2 = pd.DataFrame({'baz': [7, 8, 9, 11], 'qux': ['p', 'q', 'r', 't']})

pn = pd.Panel({'item1': df1, 'item2': df2})
print(pn)