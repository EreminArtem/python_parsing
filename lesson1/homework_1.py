"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import json

import decouple
import requests

url = 'https://api.github.com/users/EreminArtem/repos'

response = requests.get(url)

with open("repos.json", "w") as repos:
    json.dump(response.json(), repos)

"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). 
Выполнить запросы к нему, пройдя авторизацию. 
Ответ сервера записать в файл.
"""
AUTH_TOKEN = decouple.config('GITHUB_TOKEN')

get_user_url = 'https://api.github.com/user'

user_info_response = requests.get(get_user_url, headers={'Authorization': f'token {AUTH_TOKEN}'})

with open("user_info.txt", "w") as user_info:
    user_info.write(f'user: {user_info_response.json()["login"]}\n')
    user_info.write(f'avatar url: {user_info_response.json()["avatar_url"]}\n')
