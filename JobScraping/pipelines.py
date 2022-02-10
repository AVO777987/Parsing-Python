# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobscrapingPipeline:
    def __init__(self):
        pass
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.vacancies

    def process_item(self, item, spider):
        salary = self.process_salary(item.get('salary'))
        item['salary_min'], item['salary_max'], item['cur'] = salary
        del item['salary']
        collection = self.mongobase[spider.name]
        if collection.find_one({'url': item.get('url')}):
            return
        else:
            collection.insert_one(item)
        return item

    @staticmethod
    def process_salary(dirty_salary):
        if dirty_salary[0] == 'от ':
            min_salary = int(dirty_salary[1].replace('\xa0', ''))
            if dirty_salary[2] == ' до ':
                max_salary = int(dirty_salary[3].replace('\xa0', ''))
                cur = dirty_salary[5]
            else:
                max_salary = None
                cur = dirty_salary[3]
        else:
            min_salary = None
            max_salary = None
            cur = None
        return min_salary, max_salary, cur
