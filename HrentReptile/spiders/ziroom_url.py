import scrapy
from scrapy.loader import ItemLoader

from HrentReptile.items import UrlItem


class ZiroomUrl(scrapy.Spider):
    name = 'ziroom_url'
    allowed_domains = ['ziroom.com']
    start_urls = ['http://sh.ziroom.com/z/nl/z3.html']

    def parse(self, response):
        citys = list()
        for city in response.xpath('//dl[@class="changeCityList"]/dd/a'):
            href = city.xpath('./@href').extract_first()
            citys.append(href)
        with open('ziroom_urls.txt', 'w') as file:
            for city in citys:
                file.write('http:%s\n' % city)
