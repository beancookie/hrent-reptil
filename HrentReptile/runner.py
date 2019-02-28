from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from HrentReptile.spiders.baixing import BaixingSpider
from HrentReptile.spiders.ziroom import ZiroomSpider

configure_logging()
runner = CrawlerRunner()
runner.crawl(BaixingSpider)
runner.crawl(ZiroomSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
