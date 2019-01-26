# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaixingItem(scrapy.Item):
    _id = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 位置
    address = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 出租类型
    rent_type = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 装修类型
    decoration = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
