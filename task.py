import requests
import json
from bs4 import BeautifulSoup
import pandas

url = 'https://hh.ru/vacancies/sistemnyy_administrator'
params = {
    'page': 0,
    'hhtmFrom': 'vacancy_search_catalog',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

vacancys = []
vacancys_id = 0
while(True):
    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancy_list = dom.findAll('div', {'class': 'vacancy-serp-item'})
    for vacancy in vacancy_list:
        vacancys_data = {}
        info = vacancy.find('a')
        name = info.getText()
        url_vacancy = info.get('href')
        compensations = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if compensations:
            compensations = compensations.getText() \
                .replace('\u202f', '') \
                .replace('от ', '') \
                .replace('до ', '') \
                .replace('–', '') \
                .split(' ')
            for el in range(len(compensations)):
                if len(compensations) > 2:
                    compensation_min = compensations[0]
                    compensation_max = compensations[2]
                    compensation_valut = compensations[3]
                    compensation = [int(compensation_min), int(compensation_max), compensation_valut]
        else:
            compensation = None
        employer = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        if employer:
            employer = employer.getText().replace('\xa0', ' ')
        address = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
        if address:
            address = address.getText() \
                .replace('и еще', '') \
                .replace('\xa01', '') \
                .replace('\xa0', '') \
                .replace('\xa02', '')
        vacancys_data['id'] = vacancys_id
        vacancys_data['name'] = name
        vacancys_data['compensation'] = compensation
        vacancys_data['url'] = url_vacancy
        vacancys_data['employer'] = employer
        vacancys_data['address'] = address
        vacancys_data['site_name'] = 'hh.ru'
        vacancys.append(vacancys_data)
        vacancys_id += 1
    page_next = dom.find('a', {'data-qa': 'pager-next'})
    if not page_next:
        break
    params['page'] += 1

print(pandas.DataFrame(vacancys))
with open('vacancy.json', 'w', encoding='utf-8') as file:
    json.dump(vacancys, file, ensure_ascii=False)
