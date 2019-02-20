import scrapy
from HrentReptile.items import EsItem
from HrentReptile.models.ziroom.ziroom_es import ZiroomDoc


class ZiroomItem(scrapy.Item, EsItem):
    id = scrapy.Field()
    type = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 位置
    address = scrapy.Field()
    # 经纬度
    location = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 最高楼层
    top_floor = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    # 房屋配置
    deploy = scrapy.Field()
    # url
    url = scrapy.Field()
    # 交通
    traffic = scrapy.Field()
    # 室友
    chums = scrapy.Field()
    # 付款方式
    payment = scrapy.Field()
    # 推荐
    recommend = scrapy.Field()
    # 活动
    activity = scrapy.Field()
    # 空气检测
    air_part = scrapy.Field()
    # 视频
    vr_video = scrapy.Field()

    def save(self):
        ziroom = ZiroomDoc()
        ziroom.id = self['id']
        # 价格
        ziroom.price = self['price']
        # 城市
        ziroom.city = self['city']
        # 位置
        ziroom.address = self['address']
        # 经纬度
        ziroom.location = self['location']
        # 标题
        ziroom.title = self['title']
        # 户型
        ziroom.house_type = self['house_type']
        # 面积
        ziroom.area = self['area']
        # 朝向
        ziroom.orientation = self['orientation']
        # 楼层
        ziroom.floor = self['floor']
        # 最高楼层
        ziroom.top_floor = self['top_floor']
        # 标签
        ziroom.tags = self['tags']
        # 图片
        ziroom.image_urls = self['image_urls']
        # 房屋配置
        ziroom.deploy = self['deploy']
        # url
        ziroom.url = self['url']
        # 交通
        ziroom.traffic = self['traffic']
        # 室友
        ziroom.chums = self['chums']
        # 付款方式
        ziroom.payment = self['payment']
        # 推荐
        ziroom.recommend = self['recommend']
        # 活动
        ziroom.activity = self['activity']
        # 空气检测
        ziroom.air_part = self['air_part']
        # 视频
        ziroom.vr_video = self['vr_video']
        ziroom.save()
