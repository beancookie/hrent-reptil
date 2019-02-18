# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from six import string_types

import logging
import hashlib
import types


class InvalidSettingsException(Exception):
    pass


class ElasticSearchPipeline(object):
    settings = None
    es = None
    items_buffer = []

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise InvalidSettingsException('%s is not defined in settings.py' % setting_key)

        required_settings = {'ELASTICSEARCH_INDEX'}

        for required_setting in required_settings:
            validate_setting(required_setting)

    @classmethod
    def init_es_client(cls, crawler_settings):
        auth_type = crawler_settings.get('ELASTICSEARCH_AUTH')
        es_timeout = crawler_settings.get('ELASTICSEARCH_TIMEOUT',60)

        es_servers = crawler_settings.get('ELASTICSEARCH_SERVERS', 'localhost:9200')
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]

        if auth_type == 'NTLM':
            from .transportNTLM import TransportNTLM
            es = Elasticsearch(hosts=es_servers,
                               transport_class=TransportNTLM,
                               ntlm_user= crawler_settings['ELASTICSEARCH_USERNAME'],
                               ntlm_pass= crawler_settings['ELASTICSEARCH_PASSWORD'],
                               timeout=es_timeout)

            return es

        es_settings = dict()
        es_settings['hosts'] = es_servers
        es_settings['timeout'] = es_timeout

        if 'ELASTICSEARCH_USERNAME' in crawler_settings and 'ELASTICSEARCH_PASSWORD' in crawler_settings:
            es_settings['http_auth'] = (crawler_settings['ELASTICSEARCH_USERNAME'], crawler_settings['ELASTICSEARCH_PASSWORD'])

        if 'ELASTICSEARCH_CA' in crawler_settings:
            import certifi
            es_settings['port'] = 443
            es_settings['use_ssl'] = True
            es_settings['ca_certs'] = crawler_settings['ELASTICSEARCH_CA']['CA_CERT']
            es_settings['client_key'] = crawler_settings['ELASTICSEARCH_CA']['CLIENT_KEY']
            es_settings['client_cert'] = crawler_settings['ELASTICSEARCH_CA']['CLIENT_CERT']

        es = Elasticsearch(**es_settings)
        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        cls.validate_settings(ext.settings)
        ext.es = cls.init_es_client(crawler.settings)
        return ext

    def process_unique_key(self, unique_key):
        if isinstance(unique_key, list):
            unique_key = unique_key[0].encode('utf-8')
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode('utf-8')
        else:
            raise Exception('unique key must be str or unicode')

        return unique_key

    def get_id(self, item):
        item_unique_key = item[self.settings['ELASTICSEARCH_UNIQ_KEY']]
        if isinstance(item_unique_key, list):
            item_unique_key = '-'.join(item_unique_key)

        unique_key = self.process_unique_key(item_unique_key)
        item_id = hashlib.sha1(unique_key).hexdigest()
        return item_id

    def index_item(self, item, type_name):

        index_name = self.settings['ELASTICSEARCH_INDEX']
        index_suffix_format = self.settings.get('ELASTICSEARCH_INDEX_DATE_FORMAT', None)
        index_suffix_key = self.settings.get('ELASTICSEARCH_INDEX_DATE_KEY', None)
        index_suffix_key_format = self.settings.get('ELASTICSEARCH_INDEX_DATE_KEY_FORMAT', None)

        if index_suffix_format:
            if index_suffix_key and index_suffix_key_format:
                dt = datetime.strptime(item[index_suffix_key], index_suffix_key_format)
            else:
                dt = datetime.now()
            index_name += "-" + datetime.strftime(dt,index_suffix_format)
        elif index_suffix_key:
            index_name += "-" + index_suffix_key

        index_action = {
            '_index': index_name,
            '_type': type_name,
            '_source': dict(item)
        }

        if self.settings['ELASTICSEARCH_UNIQ_KEY'] is not None:
            item_id = self.get_id(item)
            index_action['_id'] = item_id
            logging.debug('Generated unique key %s' % item_id)

        self.items_buffer.append(index_action)

        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 500):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.index_item(item, spider.name)
            logging.debug('Item sent to Elastic Search %s' % spider.name)
            return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()


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
