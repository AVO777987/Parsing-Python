from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LeroyMerlin.spiders.LM import LmSpider
from LeroyMerlin import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    print('111')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, category='elektroinstrumenty')
    process.start()