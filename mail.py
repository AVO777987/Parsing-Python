from lxml import html
import requests
from pymongo import MongoClient

# База данных
client = MongoClient('127.0.0.1', 27017)
db = client['database']
news_bd = db.news

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)
news = []
urls = dom.xpath("//a[contains(@class , 'js-topnews__item')]/@href | //a[@class='list__text']/@href")
for el in urls:
    data = {}
    url = el
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    source_name = dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")
    name = dom.xpath("//h1[@class='hdr__inner']/text()")
    datetime = dom.xpath("//span[contains(@class , 'note__text')]/@datetime")
    data['name'] = name[0]
    data['url'] = url
    data['source_name'] = source_name[0]
    data['datetime'] = datetime[0]
    news_bd.insert_one(data)
