# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from bson.objectid import ObjectId


class BaixingPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.reptile
        self.collection = self.db.baixing

    def process_item(self, item, spider):
        item['_id'] = ObjectId()
        self.collection.insert_one(item)
        return item

    def close_spider(self, spider):
        self.collection.close()
        self.db.close()
        self.client.close()


if __name__ == '__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    house_db = client.reptile
    house_cl = house_db.baixing
