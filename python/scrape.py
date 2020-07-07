""" from bs4 import BeautifulSoup
import requests
import requests_cache

requests_cache.install_cache('nobel_prize', backend='sqlite', expire_after=7200)

BASE_URL = "https://en.wikipedia.org"
# A Wikipédia esetében már fontos, hogy meghatározzuk a 'User-Agent' fejlécet, amely alapján azonosítani tudja azt, hogy
# milyen rendszerből próbáljuk elérni a weboldal tartalmát
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_Nobel_soup():
    Visszatéríti az értelmezett tag fát a Nobel-díjas weboldalunkról
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

table = soup.select_one("table.sortable.wikitable")

def get_column_titles(table):
    Megszerzi a Nobel kategóriákat a table-headerekből

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

ws = get_Nobel_winners(table) """

