# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ElasticSearchPipeline(object):
    """通用的ElasticSearch存储方法"""

    def process_item(self, item, spider):
        item['type'] = spider.name
        item.save()
        return item
