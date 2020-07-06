"""

import requests

response = requests.get('https://en.wikipedia.org/wiki/Nobel_Prize')

response # output: <Response [200]>

dir(response) # output: a response objektum attribútumjai

response.headers

response.text

response = requests.get('http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10_gdp?geo=EU28&precision=1&na_item=B1GQ&unit=CP_MEUR&time=2018&time=2019')

response # output: <Response [200]>

response.json()

"""

""" 
output: 

{'version': '2.0',
 'label': 'GDP and main components (output, expenditure and income)',
 'href': 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10_gdp?geo=EU28&precision=1&na_item=B1GQ&unit=CP_MEUR&time=2018&time=2019',
 'source': 'Eurostat',
 'updated': '2020-07-01',
 'extension': {'datasetId': 'nama_10_gdp',
  'lang': 'EN',
  'description': None,
  'subTitle': None},
 'class': 'dataset',
 'value': {'0': 15915732.9, '1': 16452065.5},
 'dimension': {'unit': {'label': 'unit',
   'category': {'index': {'CP_MEUR': 0},
    'label': {'CP_MEUR': 'Current prices, million euro'}}},
  'na_item': {'label': 'na_item',
   'category': {'index': {'B1GQ': 0},
    'label': {'B1GQ': 'Gross domestic product at market prices'}}},
  'geo': {'label': 'geo',
   'category': {'index': {'EU28': 0},
    'label': {'EU28': 'European Union - 28 countries (2013-2020)'}}},
  'time': {'label': 'time',
   'category': {'index': {'2018': 0, '2019': 1},
    'label': {'2018': '2018', '2019': '2019'}}}},
 'id': ['unit', 'na_item', 'geo', 'time'],
 'size': [1, 1, 1, 2]}
"""

#######################################

"""

OECD_ROOT_URL = 'http://stats.oecd.org/sdmx-json/data'

def make_OECD_request(dsname, dimensions, params=None, root_dir=OECD_ROOT_URL):
	# Létrehozza az URL-t, majd visszatéríti a GET request válaszát 

	if not params:
		params = {}
	# azért van a fentire szükség, mert nem szabad alapértelmezett paraméterekként változtatható Python értékeket megadni

	dim_args = ['+'.join(d) for d in dimensions]
	dim_str = '.'.join(dim_args)
	# a négy dimenziós argumentumok listája, argumentumokon belül +-al összefűzve, az argumentumok sorát pedig .-al összefűzve
	# pl. AUS+AUT.GDP+B1_G3.CUR+VOBARSA.Q

	url = root_dir + '/' + dsname + '/' + dim_str + '/all'

	print('Requesting OECD URL: {}'.format(url))

	return requests.get(url, params=params)
	# a requests GET metódusa akár egy paraméter dict-et is képes bevenni, hogy az URL-t tovább alakítsa, egy URL query string-gé
	# pl. startTime=2009-Q2&endTime=2011-Q4

response = make_OECD_request('QNA', (('USA', 'AUS'), ('GDP', 'B1_GE'), ('CUR', 'VOBARSA'), ('Q')), {'startTime': '2009-Q1', 'endTime': '2010-Q1'})
# output: Requesting OECD URL: http://stats.oecd.org/sdmx-json/data/QNA/USA+AUS.GDP+B1_GE.CUR+VOBARSA.Q/all

if response.status_code == 200:
	json = response.json()
	json.keys()
	# output: dict_keys(['header', 'dataSets', 'structure'])

"""

#######################################

"""
REST_EU_ROOT_URL = 'http://restcountries.eu/rest/v1'

def REST_country_request(field='all', name=None, params=None):
	headers = {'User-Agent': 'Mozilla/5.0'}
	# legtöbbször jó ötlet az, ha meghatározzunk egy valid 'User-Agent'-et a request fejlécében,
	# annak érdekében tesszük ezt, hogy elkerüljek azt az esetet, amikor nem lehet az adatot elérni meghatározott fejléc nélkül
	# a fejlécek nem mások, mint kiegészítő információk a HTTP csatlakozás során
	# ebben az esetben az 'User-Agent' lényegében információt szolgáltat az API-nak arról, hogy milyen rendszer kéri le az információt,
	# azonosítva ez által
	
	if not params:
		params = {}
	
	if field == 'all':
		return requests.get(REST_EU_ROOT_URL + '/all')

	url = '{}/{}/{}'.format(REST_EU_ROOT_URL, field, name)
	print('Requesting URL: {}'.format(url))
	response = requests.get(url, params=params, headers=headers)
	# egy REST countries URL így néz ki: https://restcountries.eu/rest/v1/<field>/<name>?<params>

	if not response.status_code == 200:
		raise Exception('Request failed with status code {}'.format(response.status_code))
	# mielőtt visszatérítenénk a választ, megnézzük érvényes-e

	return response

response = REST_country_request('currency', 'usd')
response.json()

"""

#########################################

"""
from pymongo import MongoClient

def get_mongo_database(db_name, host='localhost', port=27017, username=None, password=None):
    if username and password:
        mongo_uri = 'mongodb://{}:{}@{}/{}'.format(username, password, host, db_name)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db_name]

db = get_mongo_database('nobel_prize')
col = db['country_data'] # egy collection az országadatokkal

# korábbi lépésben lekértük és tároltuk a response változóba a REST country request-et

col.insert_many(response.json())
# beillesztjük a kapott JSON állományt a collectionbe

res = col.find({'currencies': {'$in': ['USD']}})
list(res)
"""

########################################

"""

import json
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# fontos megjegyezni azt, hogy mindkét fenti scope-ban található API-t engedélyezni kellett a projekt service account-jára a Google APIs-ból
# tehát a Google Sheets API-t, és a Google Drive API-t

# a credentials JSON állomány a Google Services-től van
credentials = Credentials.from_service_account_file(
    "../key/pyjsviz-282509-6cfa775f3db7.json", scopes=scope
)

# ezzel hitelesítjük a hozzáférésünket a Google Spreadsheet-ekhez
gc = gspread.authorize(credentials)

# megnyitjuk az URL-vel hivatkozott Google Spreadsheet-et
ss = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1kHCEWY-d9HXlWrft9jjRQ2xf6WHQlmwyrXel6wjxkW8/edit#gid=0"
)

ss.worksheets()

ws = ss.worksheet("bugs")

ws.col_values(1)

import pandas as pd

df = pd.DataFrame(ws.get_all_records())

"""

###############################

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://en.wikipedia.org"
# A Wikipédia esetében már fontos, hogy meghatározzuk a 'User-Agent' fejlécet, amely alapján azonosítani tudja azt, hogy
# milyen rendszerből próbáljuk elérni a weboldal tartalmát
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_Nobel_soup():
    """ Visszatéríti az értelmezett tag fát a Nobel-díjas weboldalunkról """
    # egy lekérést intéz a Nobel-díjas oldalhoz, beállítva a valid Headers fejlécet

    response = requests.get(
        "{}/wiki/List_of_Nobel_laureates".format(BASE_URL), headers=HEADERS
    )

    if not response.status_code == 200:
        raise Exception(
            "Something wrong happened with status code: {}".format(response.status_code)
        )

    return BeautifulSoup(response.content, "lxml")
    # ebben az esetben már megmutatkozik az, hogy a két könyvtár képes egymás parserjét használni,
    # a második argumentum a parsert lxml-re állítja

soup = get_Nobel_soup()

soup.find("table", {"class": "wikitable sortable"})

soup.select("table.sortable.wikitable")
# ugyanazt az eredményt kapjunk, mint az előbb, azonban ebben az esetben nem okoz jövőbeli gondot az, ha a sorrend megváltozik

table = soup.select_one("table.sortable.wikitable")
table.select("th")
# a két jelölés ekvivalens
table("th")
# kiválasztja az összes table-header elemet a táblázaton belül


def get_column_titles(table):
    """ Megszerzi a Nobel kategóriákat a table-headerekből """

    cols = []

    # [1:]-vel kihagyjuk az első table-headert, mert az ugye csak a 'year'-t tartalmazza
    for th in table.select_one("tr").select("th")[1:]:
        link = th.select_one("a")
        # tárolja a kategória nevét és bármely Wikipédia linket, amit tartalmaz

        if link:
            cols.append({"name": link.text, "href": link.attrs["href"]})
        else:
            cols.append({"name": th.text, "href": None})

    return cols


def get_Nobel_winners(table):
    cols = get_column_titles(table)

    winners = []

    # kihagyjuk az első és utolsó táblázat sort, mert az a kategóriákat és a 'year'-t tartalmazza
    for row in table.select("tr")[1:-1]:
        year = int(
            row.select_one("td").text[0:4]
        )  # lekéri az első td-t, amiben az év van

        for i, td in enumerate(row.select("td")[1:]):
            for winner in td.select("a"):
                href = winner.attrs["href"]
                if not href.startswith("#endnote"):
                    winners.append(
                        {
                            "year": year,
                            "category": cols[i]["name"],
                            "name": winner.text,
                            "link": winner.attrs["href"],
                        }
                    )

    return winners


ws = get_Nobel_winners(table)

# import requests
import requests_cache

# requests_cache.install_cache()
# használjuk a továbbiakban a szokásos módon a requests könyvtárat ...

# elindít egy nobel_pages nevű cachet, sqlite backend-el és 2 órás lejárati idővel
requests_cache.install_cache('nobel_pages', backend='sqlite', expire_after=7200)

def get_winner_nationality(w):
	""" Scrapeljük az életrajzi adatokat a győztés wikipédia oldaláról """

	data = requests.get(BASE_URL + w['link'], headers=HEADERS)
	soup = BeautifulSoup(data.content, 'lxml')

	person_data = {'name': w['name']}
	attr_rows = soup.select('table.infobox tr')

	for tr in attr_rows:
		try:
			attribute = tr.select_one('th').text
			if attribute == 'Nationality':
				person_data[attribute] = tr.select_one('td').text
		except AttributeError:
			pass

	return person_data

wdata = []

for w in ws[:50]:
	wdata.append(get_winner_nationality(w))

missing_nationality = []

for w in wdata:
	if not w.get('Nationality'):
		missing_nationality.append(w)

print(missing_nationality)