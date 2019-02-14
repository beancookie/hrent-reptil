# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from HrentReptile.items import ZiroomItem


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['nj.ziroom.com']
    start_urls = ['http://nj.ziroom.com/z/nl/z2.html']

    def parse(self, response):
        houses = response.xpath('//ul[@id="houseList"]/li')
        for house in houses:
            detail_page = house.xpath('./div[@class="priceDetail"]/p[@class="more"]/a/@href').extract_first()
            yield response.follow(url='http:' + detail_page, callback=self.parse_detail)
        next_page = response.xpath('//div[@id="page"]/a[@class="next"]/@href').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = ZiroomItem()
        item['_id'] = hashlib.md5(bytes(response.url, 'utf-8')).hexdigest()
        item['url'] = response.url
        right = response.xpath('//div[@class="room_detail_right"]')
        item['title'] = right.xpath('./div[@class="room_name"]/h2/text()').extract_first().strip()
        details = right.xpath('./ul[@class="detail_room"]/li')
        item['area'] = details[0].xpath('./text()').extract_first().split()[1]
        item['orientation'] = details[1].xpath('./text()').extract_first().split()[1]
        item['house_type'] = details[2].xpath('./text()').extract_first().split()[1]
        item['floor'] = details[3].xpath('./text()').extract_first().split()[1]
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
        yield response.follow(url=price_page,
                             method='OPTIONS',
                             callback=self.parse_price,
                             meta={'data': item, 'id': id, 'house_id': house_id})

    def parse_price(self, response):
        item = response.meta['data']
        id = response.meta['id']
        house_id = response.meta['house_id']
        price = eval(response.text)['data']
        item['price'] = price['price']
        item['payment'] = price['payment']
        item['recommend'] = price['recom']
        item['recommend'] = price['recom']
        item['activity'] = price['activity_list']
        item['air_part'] = price['air_part']
        item['vr_video'] = price['vr_video']

        price_page = 'http://nj.ziroom.com/detail/config?house_id=%s&id=%s' % (house_id, id)
        yield response.follow(url=price_page,
                             method='OPTIONS',
                             callback=self.parse_deploy,
                             meta={'data': item})

    def parse_deploy(self, response):
        item = response.meta['data']
        deploy = eval(response.text)['data']
        item['deploy'] = deploy
        yield item
