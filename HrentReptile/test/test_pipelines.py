import unittest

import scrapy

from HrentReptile.pipelines import MongoPipeline


class MyTest(unittest.TestCase):

    def test_save(self):
        pipeline = MongoPipeline()
        item = {'_id': 'b9f353d3679b46bd45aa26de5988f48', 'title': 'test_title'}
        spider = scrapy.spiders.Spider('ziroom')
        self.assertNotEquals(None, pipeline.process_item(item, spider))
