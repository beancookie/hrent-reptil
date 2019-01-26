# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BaixingPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://hrent:hrent@193.112.33.124/?authSource=hrent&authMechanism=SCRAM-SHA-256')
        self.db = self.client.hrent
        self.collection = self.db.baixing

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item

    def close_spider(self, spider):
        self.collection.close()
        self.db.close()
        self.client.close()
