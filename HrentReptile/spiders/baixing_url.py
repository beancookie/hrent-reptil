import scrapy
from scrapy.loader import ItemLoader

from HrentReptile.items import UrlItem


class BaixingUrl(scrapy.Spider):
    name = 'baixing_url'
    allowed_domains = ['baixing.com']
    start_urls = ['http://www.baixing.com/?changeLocation=yes&return=%2Fzhengzu%2F%3Fsrc%3Dtopbar']

    def parse(self, response):
        loader = ItemLoader(item=UrlItem(), response=response)
        citys = list()
        for city in response.xpath('//a'):
            href = city.xpath('./@href').extract_first()
            if href is not None and 'topbar' in href:
                citys.append(href)
        with open('baixing_urls.txt', 'w') as file:
            for city in citys:
                file.write('http:%s\n' % city)
