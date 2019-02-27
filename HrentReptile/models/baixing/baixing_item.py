import scrapy
from HrentReptile.items import EsItem
from HrentReptile.models.baixing.baixing_es import BaixingDoc


class BaixingItem(scrapy.Item, EsItem):
    id = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 位置
    address = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()
    # 经纬度
    location = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 出租类型
    rent_type = scrapy.Field()
    # 细节
    decorate = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 最高层
    top_floor = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()

    def save(self):
        baixing = BaixingDoc()
        baixing.id = self['id']
        baixing.url = self['url']
        # 价格
        baixing.price = self['price']
        # 城市
        baixing.city = self['city']
        # 位置
        baixing.address = self['address']
        # 更新时间
        baixing.update_date = self['update_date']
        # 经纬度
        baixing.location = self['location']
        # 标题
        baixing.title = self['title']
        # 户型
        baixing.house_type = self['house_type']
        # 出租类型
        baixing.rent_type = self['rent_type']
        # 装修类型
        baixing.decorate = self['decorate']
        # 面积
        baixing.area = self['area']
        # 朝向
        baixing.orientation = self['orientation']
        # 更新时间
        baixing.update_date = self['update_date']
        # 楼层
        baixing.floor = self['floor']
        # 标签
        baixing.tags = self['tags']
        # 图片
        baixing.image_urls = self['image_urls']
        baixing.save()

