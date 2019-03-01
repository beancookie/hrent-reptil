# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ElasticSearchPipeline(object):
    """通用的ElasticSearch存储方法"""

    def process_item(self, item, spider):
        item['type'] = spider.name
        item.save()
        return item


class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://hrent:hrent@193.112.33.124/?authSource=hrent&authMechanism=SCRAM-SHA-256')
        self.db = self.client.hrent

    def process_item(self, item, spider):
        collection = self.db.get_collection(spider.name)

        is_update = (collection.find_one_and_replace({'_id': item['_id']}, item) != None)
        if not is_update:
            collection.insert_one(item)
        return item

    def close_spider(self, spider):
        self.db.close()
        self.client.close()


