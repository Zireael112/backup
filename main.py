import json
import time
import requests
from pprint import pprint

with open('token.txt', 'r') as file:
    VK_TOKEN = file.read().strip()

URL = 'https://api.vk.com/method/'
#375505257
VK_USER_ID = input('Введите id профиля с которого необходимо скачать фотографии: ')

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
def get_largest_photo():
    data = get_photo()
    count_photo = data['response']['count']
    i = 0
    count = 50
    photos = {}
    while i <= count_photo:
        if count_photo == 0:
            print('Фотографии(ия) не найдены(а)!')
            break
        if i != 0:
            data = get_photo(offset=i, count=count)
        for files in data['response']['items']:
            file_url = files['sizes'][-1]['url']
            filename = files['likes']['count']
            filename_wb = file_url.split('/')[-1].split('?')[0]
            photos[filename] = file_url
            time.sleep(0.1)
            res = requests.get(file_url)

            with open('images/%s' % filename_wb, 'wb') as file_wr:
                file_wr.write(res.content)
        i += count

    pprint(photos)

# pprint(get_photo())
get_largest_photo()

