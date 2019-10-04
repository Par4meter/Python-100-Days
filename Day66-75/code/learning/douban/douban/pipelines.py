# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.exceptions import DropItem


class DoubanPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.collection = connection.douban.movie

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                raise DropItem(f'Missing {data} of blogpost from {item["url"]}')
        if valid:
            new_movie = [{
                'name': item['name'],
                'score': item['score'],
                'classification': item['classification'],
                'actor': item['actor'],
            }]
            self.collection.insert(new_movie)
            print('Item wrote to Mongo')
        return item
