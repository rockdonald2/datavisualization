import scrapy
import re

BASE_URL = 'http://en.wikipedia.org'

class NWinnerItemBio(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()

class NWinnerSpiderBio(scrapy.Spider):
    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.NobelImagesPipeline': 1,}
    }

    def parse(self, response):
        filename = response.url.split('/')[-1]
        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('//span[@class="mw-headline"]/text()').extract()

            if country:
                winners = h3.xpath('following-sibling::ol[1]')

                for w in winners.xpath('li'):
                    wdata = {}

                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]

                    request = scrapy.Request(wdata['link'], callback=self.get_mini_bio)

                    request.meta['item'] = NWinnerItemBio(**wdata)

                    yield request

    def get_mini_bio(self, response):
        """ Lekéri a győztes életrajzi-szövegét és képét """

        BASE_URL_ESCAPED = 'http:\/\/en.wikipedia.org'

        item = response.meta['item']

        item['image_urls'] = []

        img_src = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[2]/td/a/img/@src')

        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()]

        mini_bio = ''
        # eltérünk a könyv xpath-jétől, hiszen a mi esetünkben nincs az az üres para, amivel ő áll meg
        # nekünk a content-text-en belüli összes elem kell, hogy megkeressük a megállást jelentő tartalomjegyzéket
        tags = response.xpath('//*[@id="mw-content-text"]/div/*').extract()

        for t in tags:
            # ahhoz, hogy megkapjuk a keresett jegyzéket, regExp-et használunk
            if re.findall('id="toc"', t):
                break

            # muszáj volt belerakjam a korlátozást a stringbe, másképp néha megbolondult
            if not re.findall('<p>', t[:16]):
                continue

            # mivel a mi esetünkben nyersnek vannak meg a tag-ek, jobb, ha a paragrafus tageket eltávolítjuk
            tmp = re.sub('<p>|</p>', '', t)
            mini_bio += tmp

        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#', item['link'] + '#')

        item['mini_bio'] = mini_bio

        yield item