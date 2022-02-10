import scrapy
from scrapy.http import HtmlResponse
from JobScraping.items import JobscrapingItem


class SjruSpider(scrapy.Spider):
    name = 'SJRU'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/sistemnyj-administrator.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[contains(@class, 'f-test-vacancy-item')]/div/div/div/div/span/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/span").getall()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobscrapingItem(name=name, salary=salary, url=url)
