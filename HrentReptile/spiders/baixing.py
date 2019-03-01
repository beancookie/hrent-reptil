# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import os
from HrentReptile.models.baixing.baixing_item import BaixingItem
from HrentReptile.utils.map_util import geocode
from HrentReptile.utils.str_util import get_int, get_float, get_date


class BaixingSpider(scrapy.Spider):
    name = 'baixing'
    allowed_domains = ['baixing.com']
    start_urls = [url.strip() for url in open('%s_urls.txt' % name).readlines()]
    detail_keys = ['rent_type', 'house_type', 'area', 'decorate', 'orientation', 'top_floor']

    # def start_requests(self):

    def parse(self, response):
        houses = response.xpath('//ul[@class="list-ad-items has-melior-fang"]/li')
        for house in houses:
            item = BaixingItem()
            item['city'] = response.xpath('//a[@class="hot-link"]/text()').extract_first()
            item['title'] = house.xpath('./div[@class="media-body"]/div[1]/a[@class="ad-title"]/text()').extract_first()
            item['price'] = get_int(house.xpath('./div[@class="media-body"]/div[1]/span/text()').extract_first(), verify=False)
            item['tags'] = house.xpath('./div[@class="media-body"]/div[1]/a[@data-toggle="tooltip"]/text()').extract() \
                           + house.xpath('./div[@class="media-body"]/div[1]/a[contains(@class, "tag-vip")]/@data-original-title').extract()

            details = house.xpath('./div[@class="media-body"]/div[2]/text()').extract_first('').split('/')
            details = list(map(lambda x: x.strip(), details))
            for i, detail in enumerate(details):
                if self.detail_keys[i] == 'area':
                    item[self.detail_keys[i]] = get_float(detail, verify=False)
                elif self.detail_keys[i] == 'top_floor':
                    if detail is not None:
                        item[self.detail_keys[i]] = get_int(detail, verify=False)
                        item['floor'] = detail
                else:
                    item[self.detail_keys[i]] = detail
            item['address'] = house.xpath('./div[@class="media-body"]/div[3]/text()').extract_first()
            item['location'] = geocode(item['city'], item['address'])
            item['update_date'] = get_date(house.xpath('./div[@class="media-body"]/div[3]/time/text()').extract_first())
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
