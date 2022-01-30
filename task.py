from pprint import pprint
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# База данных
client = MongoClient('127.0.0.1', 27017)
db = client['database']
vacancy_bd = db.vacancy

# Параметры парсера
url = 'https://hh.ru/vacancies/sistemnyy_administrator'
params = {
    'page': 0,
    'hhtmFrom': 'vacancy_search_catalog',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}


def vacancy_append_bd(vacancys_data):
    if vacancy_bd.find_one({'url': vacancys_data.get('url')}):
        return
    else:
        vacancy_bd.insert_one(vacancys_data)


def get_compensations(value):
    for doc in vacancy_bd.find({'compensation': {'$gte': value}}):
        pprint(doc)


def vacancy_searche():
    while True:
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
                        compensation_min = compensations[0]
                        compensation_max = None
                        compensation_valut = compensations[1]
                        compensation = [int(compensation_min), compensation_max, compensation_valut]
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
            vacancys_data['name'] = name
            vacancys_data['compensation'] = compensation
            vacancys_data['url'] = url_vacancy
            vacancys_data['employer'] = employer
            vacancys_data['address'] = address
            vacancys_data['site_name'] = 'hh.ru'
            vacancy_append_bd(vacancys_data)
        page_next = dom.find('a', {'data-qa': 'pager-next'})
        if not page_next:
            break
        params['page'] += 1


while True:
    print('1. Поиск новых вакансий на сайте hh.ru')
    print('2. Посмотреть вакансии с зарплатой больше заданной')
    print('3. Выход из программы')
    menu_input = input('Введите то что хотите сделать\n')
    if menu_input == '1':
        vacancy_searche()
    if menu_input == '2':
        try:
            value = 0
            value = int(input('Введите зарплату'))
        except ValueError:
            print('Вы ввели не число!')
        get_compensations(value)
    if menu_input == '3':
        break
