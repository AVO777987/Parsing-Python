# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class LeroymerlinPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.leroy_base = client.LeroyMerlin

    def process_item(self, item, spider):
        try:
            collection = self.leroy_base[spider.name]
            if collection.find_one({'url': item.get('url')}):
                return item
            else:
                collection.insert_one(item)
            return item
        except Exception as error:
            print(error)
        return item


class LeroymerlinImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{str(item.get("name"))}/{image_guid}.jpg'
