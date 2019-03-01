# -*- coding: utf-8 -*-
import json

import scrapy
import hashlib
import re

from scrapy import Request

from HrentReptile.models.ziroom.ziroom_item import ZiroomItem
from HrentReptile.utils.map_util import geocode
from HrentReptile.utils.ocr_util import image_to_string
from HrentReptile.utils.str_util import get_float, get_int, get_city_from_url


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = [url.strip() for url in open('%s_urls.txt' % name).readlines()]

    def parse(self, response):
        houses = response.xpath('//ul[@id="houseList"]/li')
        for house in houses:
            detail_page = house.xpath('./div[@class="priceDetail"]/p[@class="more"]/a/@href').extract_first()
            yield Request(url='http:' + detail_page, callback=self.parse_detail)
        next_page = response.xpath('//div[@id="page"]/a[@class="next"]/@href').extract_first()

        if next_page is not None:
            yield Request(url='http:%s' % next_page, callback=self.parse)

    def parse_detail(self, response):
        item = ZiroomItem()
        item['_id'] = hashlib.md5(bytes(response.url, 'utf-8')).hexdigest()
        item['url'] = response.url
        item['city'] = response.xpath('//span[@id="curCityName"]/text()').extract_first()
        item['detail'] = response.xpath('//div[@class="aboutRoom gray-6"]/p/text()').extract_first()
        right = response.xpath('//div[@class="room_detail_right"]')
        item['title'] = right.xpath('./div[@class="room_name"]/h2/text()').extract_first()
        if item['title']:
            item['title'] = item['title'].strip()
        item['address'] = re.split('\\d+', item['title'])[0]
        if item['city'] is None:
            item['city'] = get_city_from_url(item['url'])
        item['location'] = geocode(item['city'], item['address'])
        details = right.xpath('./ul[@class="detail_room"]/li')
        item['area'] = get_float(details[0].xpath('./text()').extract_first().split()[1])
        item['orientation'] = details[1].xpath('./text()').extract_first().split()[1]
        item['house_type'] = details[2].xpath('./text()').extract_first().split()[1]
        floor = details[3].xpath('./text()').extract_first().split()[1]
        item['floor'] = get_int(floor.split('/')[0])
        top_floor = floor.split('/')[1]
        item['top_floor'] = get_int(top_floor[0:len(top_floor) - 1])
        traffic = details[4].xpath('string(.)').extract_first().split()
        item['traffic'] = traffic[1:len(traffic)]
        item['tags'] = response.xpath('//p[@class="room_tags clearfix"]/span').xpath('string(.)').extract()
        item['chums'] = []
        chums = response.xpath('//div[@class="greatRoommate"]/ul/li')
        for chum in chums:
            gender = chum.xpath('./@class').extract_first().strip()
            if gender.find('current') != -1:
                item['chums'].append({'state': '可入住', 'bedroom': chum.xpath('./div/div[1]/p/text()').extract_first()})
            else:
                chum_dict = {'bedroom': chum.xpath('./div/div[1]/p/text()').extract_first(),
                           'state': chum.xpath('.//span[@class="tags"]/text()').extract_first(),
                           'sign': chum.xpath('.//p[@class="sign"]/text()').extract_first(),
                           'job': chum.xpath('.//span[@class="ellipsis"]/text()').extract_first(),
                           'check_in_time': chum.xpath('./div/div[3]/p/text()').extract_first().strip(),
                           'gender': gender}
                if chum_dict['job'] == '...':
                    chum_dict['job'] = '未知'

                item['chums'].append(chum_dict)

        item['image_urls'] = []
        images = response.xpath('//ul[@class="lof-main-wapper"]/li')
        for images in images:
            item['image_urls'].append('http:' + images.xpath('.//img/@src').extract_first())

        id = response.xpath('//input[@id="room_id"]/@value').extract_first()
        house_id = response.xpath('//input[@id="house_id"]/@value').extract_first()
        price_page = 'http://nj.ziroom.com/detail/info?id=%s&house_id=%s' % (id, house_id)
        yield Request(url=price_page,
                             method='OPTIONS',
                             callback=self.parse_price,
                             meta={'data': item, 'id': id, 'house_id': house_id})
        
    @staticmethod
    def get_price_from_image(url, codes):
        text = image_to_string(url)
        price = []
        for code in codes:
            price.append(text[code])
        return ''.join(price)

    def parse_price(self, response):
        item = response.meta['data']
        id = response.meta['id']
        house_id = response.meta['house_id']
        price = json.loads(response.body)['data']
        item['price'] = get_int(self.get_price_from_image('http:' + price['price'][0], price['price'][2]))
        item['original_price'] = price['price']
        item['original_payment'] = price['payment']
        item['payment'] = []
        for payment in price['payment']:
            payment_dict = {
                'period': payment['period'],
                'price': get_int(self.get_price_from_image('http:' + payment['rent'][0], payment['rent'][2]))
            }
            item['payment'].append(payment_dict)

        item['recommend'] = []
        for recommend in price['recom']:
            recommend_dict = {
                'url': recommend['url'],
                'photo': recommend['photo'],
                'info': recommend['info'],
                'price': get_int(self.get_price_from_image('http:' + recommend['price'][1], recommend['price'][2])),
                'district': recommend['district'],
            }
            item['recommend'].append(recommend_dict)

        item['activity'] = price['activity_list']
        item['air_part'] = price['air_part']
        item['vr_video'] = price['vr_video']

        price_page = 'http://nj.ziroom.com/detail/config?house_id=%s&id=%s' % (house_id, id)
        yield Request(url=price_page,
                             method='OPTIONS',
                             callback=self.parse_deploy,
                             meta={'data': item})

    def parse_deploy(self, response):
        item = response.meta['data']
        deploy = json.loads(response.body)['data']
        item['deploy'] = deploy
        yield item
