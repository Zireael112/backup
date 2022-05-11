import json
import time
import requests
from pprint import pprint
import yadisk


# Функция для запроса словаря с данными
def get_photo(offset=0, count=50):
    params = {
        'owner_id': VK_USER_ID,
        'album_id': 'profile',
        'access_token': VK_TOKEN,
        'offset': offset,
        'v': '5.131',
        'count': count,
        'extended': 1,
        'photo_sizes': 1,
    }

    res = requests.get(URL + 'photos.get', params=params).json()
    return res


# Функция для сохранения фото самого большого разрешения в папку images
def get_largest_photo_and_load_on_disk():
    data = get_photo()
    count_photo = data['response']['count']
    i = 0
    count = 50

    while i <= count_photo:
        if count_photo == 0:
            print('Фотографии(ия) не найдены(а)!')
            break
        if i != 0:
            data = get_photo(offset=i, count=count)

        # Вынимаем название(лайки) и фото наибольшего размера.
        for files in data['response']['items']:
            file_url = files['sizes'][-1]['url']
            filename = files['likes']['count']
            filename_wb = file_url.split('/')[-1].split('?')[0]
            time.sleep(0.1)
            res = requests.get(file_url)

            with open('images/' + filename_wb, 'wb') as file_wr:
                file_wr.write(res.content)

            # Создаем папку на яндекс диске
            try:
                link_load.mkdir('/Photos')
                print('Создана папка Photos')
            except:
                print('Фото загружается...')

            # Записываем фото на яндекс диск
            try:
                link_load.upload('images/' + filename_wb, '/Photos/' + str(filename))
                print('Фото загружено...\n')
            except yadisk.exceptions.PathExistsError:
                print(f'Произошёл конфлик в связи с одинаковым названием файлов, файл {file_url} будет перезаписан')
                continue

        i += count


# # Переменные

# Данные для вк
with open('token.txt', 'r') as file:
    VK_TOKEN = file.read().strip()

URL = 'https://api.vk.com/method/'

# Универсальный id - 375505257
VK_USER_ID = input('Введите id профиля с которого необходимо скачать фотографии: ')
token = 'AQAAAABfGD2GAAfkONDLMqFw1EXKq4hOt5OVxG8'
link_load = yadisk.YaDisk(token=token)

get_largest_photo_and_load_on_disk()
print('Все файлы загружены!')
