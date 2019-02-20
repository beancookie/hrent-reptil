import scrapy
from HrentReptile.items import EsItem
from HrentReptile.models.ziroom.ziroom_es import ZiroomDoc


class BaixingItem(scrapy.Item, EsItem):
    pass
