import requests
import json

url = 'https://api.vk.com/method/users.getSubscriptions'


def get_user_group_vk(users_param):
    print(users_param)
    response = json.loads(requests.get(url, params=users_param).content)
    return response


def save_repository_to_json(data):
    with open('group_vk.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    users_param = {
        'user_id': '1501872',
        'extended': 1,
        'access_token': '#acces_token',
        'v': '5.131'
    }
    data = get_user_group_vk(users_param)
    save_repository_to_json(data)

