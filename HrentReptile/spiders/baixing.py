# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import hashlib
from HrentReptile.items import BaixingItem


class BaixingSpider(scrapy.Spider):
    name = 'baixing'
    allowed_domains = ['nanjing.baixing.com']
    start_urls = ['http://nanjing.baixing.com/zhengzu/']
    detail_keys = ['rent_type', 'house_type', 'area', 'decoration', 'orientation', 'floor']

    def parse(self, response):
        houses = response.xpath('//ul[@class="list-ad-items has-melior-fang"]/li')
        for house in houses:
            item = BaixingItem()
            item['title'] = house.xpath('./div[@class="media-body"]/div[1]/a[@class="ad-title"]/text()').extract_first()
            item['price'] = house.xpath('./div[@class="media-body"]/div[1]/span/text()').extract_first()
            item['tags'] = house.xpath('./div[@class="media-body"]/div[1]/a[@data-toggle="tooltip"]/text()').extract() \
                           + house.xpath('./div[@class="media-body"]/div[1]/a[contains(@class, "tag-vip")]/@data-original-title').extract()

            details = house.xpath('./div[@class="media-body"]/div[2]/text()').extract_first('').split('/')
            details = list(map(lambda x: x.strip(), details))
            for i, detail in enumerate(details):
                item[self.detail_keys[i]] = detail
            item['address'] = house.xpath('./div[@class="media-body"]/div[3]/text()').extract_first()
            item['update_date'] = house.xpath('./div[@class="media-body"]/div[3]/time/text()').extract_first()
            detail_page = house.xpath('./a[1]/@href').extract_first()
            yield response.follow(url=detail_page, callback=self.parse_detail, meta={'data': item})

        next_page = response.xpath('//ul[@class="list-pagination"]/li[not(@class="active")][last()]').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['data']
        item['_id'] = hashlib.md5(bytes(response.url, 'utf-8')).hexdigest()
        item['url'] = response.url
        images = response.xpath('//div[@class="featured-height"]/div')
        item['image_urls'] = []
        for image in images:
            original_url = image.xpath('./a/@style').extract_first()
            url = re.findall(r'[(](.*?)[)]', original_url)[0]
            if url:
                item['image_urls'].append(url)
        yield item
