# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NobelWinnersPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exceptions import DropItem

class DropNonPerson(object):
    """ Törölje a nem-egyén győzteseket """

    def process_item(self, item, spider):
        if not item['gender']:
            # abban az esetben, ha a scrapelt elemünkben nem található gender, abban az esetben egy egyesületről beszélhetünk
            # mivel a végső vizualizációnk a személyekre összpontosít, ezért a DropItem-el elvetjük az elemet az output streamből
            raise DropItem('A következő győztes nem személy: {}'.format(item['name']))

        # muszáj visszatérítenünk az elemet a metódusból, további pipeline-ok miatt vagy akár azért, mert a Scrapy-nek lekell mentenie
        return item

from scrapy.pipelines.images import ImagesPipeline

class NobelImagesPipeline(ImagesPipeline):
    # bevesz bármilyen kép URL, amit az nwinners_minibio spider scrapelt és generál egy HTTP lekérdezést a tartalmára
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'dont_redirect': False})

    # miután legenerálódott a lekérdezés, ennek eredménye ebbe a metódusba kerül
    def item_completed(self, results, item, info):
        # Mivel, az eredmény tuple-kbe van rendezve a következő formában: [(True, Image), (False, Image)]
        # kiszűrjük azokat az eseteket, amikor nem sikerült a képet lekérni
        image_paths = [x['path'] for ok, x in results if ok]

        # azoknál, amelyeknél sikerült, lementi a elérésüket, ahhoz a mappához viszonyítva, amelyet
        # a settings.py-ban határoztunk meg:
        # IMAGES_STORE = 'images'
        # ITEM_PIPELINES = {
        # 'nobel_winners.pipelines.DropNonPerson': 1, # az 1-essel aktíváljuk a pipeline-t
        # 'nobel_winners.pipelines.NobelImagesPipeline': 1,
        # }
        if image_paths:
            item['bio_image'] = image_paths[0]

        return item
