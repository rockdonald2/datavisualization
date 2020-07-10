import scrapy
import re

""" 

class NWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()

class NWinnerSpider(scrapy.Spider):
    Megszerzi az országneveket és a link texteket a Nobel-győzteseknek

    name = 'nwinners_list'

    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    def parse(self, response):
        h3s = response.xpath('//h3')
        # megszerezzük az összes <h3>-at a weboldalon, a legtöbb ilyen az országneveket tartalmazza

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            # ahol lehetséges, megszerzi a <h3> elem azon child <span>-jét, amely rendelkezik az mw-headline classal

            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                # megszerzi a h3-at követő rendezett listát, amely a nyerteseket tartalmazza

                for w in winners.xpath('li'):
                    # a listán végighaladva megszerzi a <li>-ben található szöveget

                    text = w.xpath('descendant-or-self::text()').extract()

                    # majd téríti a találatokat, de yield segítségével, amely lehetőséget biztosít arra, hogy úm. szüneteltessük a függvényt és megőrzi állapotát ahová visszatérhet
                    # a végrehajtás
                    yield NWinnerItem(country = country[0], name=text[0], link_text = ' '.join(text))


"""


class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()


''' class NWinnerSpider(scrapy.Spider):
    """ Megszerzi a NWinnerItem-ben meghatározott adatokat """

    name = "nwinners_list"

    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    def parse(self, response):
        h3s = response.xpath("//h3")

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()

            if country:
                winners = h3.xpath("following-sibling::ol[1]")

                for w in winners.xpath("li"):
                    wdata = process_winner_li(w, country[0])

                    yield NWinnerItem(
                        name=wdata["name"],
                        link=wdata["link"],
                        year=wdata["year"],
                        category=wdata["category"],
                        country=wdata["country"],
                        born_in=wdata["born_in"],
                        text=wdata["text"],
                    ) '''


BASE_URL = "http://en.wikipedia.org"


def process_winner_li(w, country=None):
    """ Feldolgozza a győztes <li> tagjét, hozzáadva a születési országot vagy nemzetiséget, ha lehetséges """

    wdata = {}

    # azért van szükség az egyenlőség jobb oldalán található részre, mert a href a következő alakot veszi fel a wiki-n: /wiki/...
    # a xpath segítségével megkeressük azt az anchor taget, amely rendelkezik hivatkozási linkkel
    wdata["link"] = BASE_URL + w.xpath("a/@href").extract()[0]

    # kiveszi a teljes szöveget a <li>-ből, majd a nevet kiválasztja ebből a sorból
    text = " ".join(w.xpath("descendant-or-self::text()").extract())
    wdata["name"] = text.split(",")[0].strip()

    # regExp, amely megtalál a stringben egy olyan match-et, amely 4 számból áll
    year = re.findall("\d{4}", text)

    if year:
        wdata["year"] = int(year[0])
    else:
        wdata["year"] = 0
        print("No year in ", text)

    # regExp, amely kiválasztja a kategóriát
    category = re.findall(
        "Physics|Chemistry|Physiology or Medicine|Physiology|Medicine|Literature|Peace|Economics", text
    )

    if category:
        wdata["category"] = category[0]
    else:
        wdata["category"] = ""
        print("No category in ", text)

    if country:
        # a csillaggal jelölték azt a wiki-n, ha valaki az adott országban született, de más nemzetiségű
        if text.find("*") != -1:
            wdata["country"] = ""
            wdata["born_in"] = country
        else:
            wdata["country"] = country
            wdata["born_in"] = ""

    # lementünk egy másolatot a szövegből, hogy akár később manuálisan is tudjunk az adatokon korrigálni
    wdata["text"] = text
    return wdata


class NWinnerSpider(scrapy.Spider):
    name = "nwinners_full"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.DropNonPerson': 1,}
    }

    def parse(self, response):
        filename = response.url.split("/")[-1]

        # lekéri az összes h3 taget az oldalról
        h3s = response.xpath("//h3")

        # jelenleg csak az első 3 országot fogjuk megszerezni, már nem igaz
        for h3 in h3s:
            # megszerezzük az országot, és ki is bontjuk, megszerezve a teljes tartalmát
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()

            # ha az országnak nincs valid tartalma, ne csináljon semmit
            if country:
                # megszerezzük a nyertesek listáját
                winners = h3.xpath("following-sibling::ol[1]")

                # a lista elemein végighaladva megszerezzük az adatokat
                for w in winners.xpath("li"):
                    # feldolgozzuk a lista elemet megszerezve az alapvető adatokat, amelyek a Nobel-díjas oldalról kinyerhetők
                    wdata = process_winner_li(w, country[0])

                    # a további, hiányzó adatokat request láncolással oldjuk meg
                    # a request funkció egy request-et csinál a győztes Wikipédia oldalára, felhasználva a wdata-ban található hyperlinket
                    # a callback függvényt állítsuk be a második argumentumban, amely az első argumentumra címezett request válaszát fogja megkapni majd feldolgozni
                    request = scrapy.Request(
                        wdata["link"], callback=self.parse_bio, dont_filter=True
                    )

                    # létrehozunk egy Scrapy Itemet, amely tartalmazni fogja a Nobel adatunkat
                    # aztán ez az Item adat hozzárendelődik a request metaadatjához, hogy bármiféle válasz hozzáférést biztosítson
                    request.meta["item"] = NWinnerItem(**wdata)

                    # az által, hogy yield-eljük a request-et, a parse metódus egy generátorrá válik, amely felhasználható request-eket térít
                    yield request

    # ez a metódus fogja kezelni a életrajzi oldalra címzett lekérdez call-backjét
    def parse_bio(self, response):
        # ahhoz, hogy hozzáadjuk a scrapelt adatunkat a Scrapy Itemhez, először lekérjük azt a response metaadatjából
        item = response.meta["item"]

        # megkapja a linket az életrajzi oldal Wikidata oldalához
        href = response.xpath('//li[@id="t-wikibase"]/a/@href').extract()

        if href:
            # felhasználja a Wikidata linket ahhoz, hogy generáljon egy lekérdezést a Spider-ünk parse_wikidata metódusával, mint callback függvény
            request = scrapy.Request(
                href[0], callback=self.parse_wikidata, dont_filter=True
            )

            request.meta["item"] = item

            yield request

    def parse_wikidata(self, response):
        item = response.meta["item"]

        # a releváns adatok tartalmazó kódok, amik a Wikidata forrásából vannak, a nevük megegyezik a Scrapy Itemükben meghatározott nevekkel,
        # azok amelyek link attribútummal is rendelkeznek linkként vannak meghatározva a wikin
        property_codes = [
            {"name": "date_of_birth", "code": "P569"},
            {"name": "date_of_death", "code": "P570"},
            {"name": "place_of_birth", "code": "P19", "link": True},
            {"name": "place_of_death", "code": "P20", "link": True},
            {"name": "gender", "code": "P21", "link": True},
        ]

        # ez a szépség a Chrome DevTools-ból való
        # alakítani kellett, hiszen megváltozott a wikidata oldala a könyvhöz képest
        # //*[@id="P21"]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/a/text()
        p_template = (
            '//*[@id="{code}"]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]{link_html}/text()'
        )

        for prop in property_codes:
            link_html = ""

            if prop.get("link"):
                link_html = "/a"

            # kiegészítjük a fenti template selectorunkat a hiányos részekkel, a format függvényt használva
            # hozzáadva a szükség /a-t amennyiben linkbe van ágyazva a Wikin a mező
            sel = response.xpath(
                p_template.format(code=prop["code"], link_html=link_html)
            )

            if sel:
                item[prop["name"]] = sel[0].extract()
            else:
                item[prop["name"]] = ""

        # végül yieldeljük az item-et, amely ezen a ponton már minden adatot tartalmaznia kellene a wiki-ről
        yield item
