# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaseItem(scrapy.Item):
    id = scrapy.Field()
    _type = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 位置
    address = scrapy.Field()
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
    # 标签
    tags = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    # 房屋配置
    deploy = scrapy.Field()
    # url
    url = scrapy.Field()

class BaixingItem(BaseItem):
    # 出租类型
    rent_type = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()
    # 装修类型
    decoration = scrapy.Field()


class ZiroomItem(BaseItem):
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

