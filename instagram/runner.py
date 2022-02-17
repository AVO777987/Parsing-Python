from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram.spiders.instaspider import InstaspiderSpider
from instagram import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaspiderSpider)

    process.start()

