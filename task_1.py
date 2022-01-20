import requests
import json

url = 'https://api.github.com/users'


def get_user_repository(user):
    user_url = f'{url}/{user}/repos'
    print(user_url)
    response = json.loads(requests.get(user_url).content)
    return response


def save_repository_to_json(data):
    with open('repository.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)


if __name__ == '__main__':
    data = get_user_repository('AVO777987')
    save_repository_to_json(data)
