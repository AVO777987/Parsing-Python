from lxml import html
import requests
from pymongo import MongoClient

# База данных
client = MongoClient('127.0.0.1', 27017)
db = client['database']
news_bd = db.news

url_source = 'https://lenta.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url_source, headers=headers)

dom = html.fromstring(response.text)
news = []
items = dom.xpath("//a[contains(@class, '_topnews')]")
for item in items:
    data = {}
    url = f'{url_source}{item.xpath("@href")[0]}'
    if item.xpath(".//h3/text()"):
        name = item.xpath(".//h3/text()")
        datetime = item.xpath(".//time[@class='card-big__date']/text()")
    else:
        name = item.xpath(".//span[@class='card-mini__title']/text()")
        datetime = item.xpath(".//time[@class='card-mini__date']/text()")
    source_name = 'Лента Ру'
    data['name'] = name[0]
    data['url'] = url
    data['source_name'] = source_name
    data['datetime'] = datetime[0]
    news_bd.insert_one(data)
