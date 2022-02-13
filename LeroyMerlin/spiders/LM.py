import scrapy
from scrapy.http import HtmlResponse
from items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'LM'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{kwargs.get("category")}/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@data-origin")
        loader.add_value('url', response.url)
        yield loader.load_item()
