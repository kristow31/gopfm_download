import datetime
import json

import vk_api
from vk_api import audio
import requests
import time
import os
from tqdm import tqdm
import re

REQUEST_STATUS_CODE = 200
name_dir = 'mp3'
path = r'D:\PycharmProjects\GOP_FM\\' + name_dir
login = '********'  # Номер телефона
password = '*********'  # Пароль
my_id = '*********'  # Ваш id vk

if not os.path.exists(path):
    os.makedirs(path)

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def save_file(file, txt):
    try:
        with open(file, 'a') as f:
            f.write(txt + "\r")
    except:
        print("Ошибка записи в файл: ", file)

def load_playlist():
    with open('playlist.txt', 'rb') as f:
        result = f.read()
        return json.loads(result)

# Поиск музыки
def search(name_audio):

    os.chdir(path)
    song = 0
    error = True
    time_start = datetime.datetime.now()
    for i in vk_audio.search(name_audio, count=20):
        try:
            song += 1
            r = requests.get(i['url'], stream=True)
            if 'Content-Length' not in r.headers:
                print('NET Content-Length | ', song)
                continue
            size = int(r.headers['Content-Length'])
            if r.status_code == 200:
                muzika = emoji_pattern.sub(r'', i['artist'] + ' - ' + i['title'])
                if 'минус' in muzika.lower() or 'dj' in muzika.lower():
                    print('NE TO >>> ', i['artist'] + ' - ' + i['title'])
                    continue
                if not os.path.exists(muzika + '.mp3'):
                    with open(muzika + '.mp3', 'wb') as file:
                        print('Загрузка:', muzika)
                        time.sleep(0.5)
                        error = False
                        save_file('good.txt', muzika)
                        for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size / 1024, unit='KB',
                                         leave=True):
                            file.write(data)
                else:
                    error = False
                break
        except OSError:
            print('Ошибка загрузки:', song, i['artist'] + ' - ' + i['title'])

    time_end = datetime.datetime.now()
    print('Загружено', len(next(os.walk(path))[2]), 'песен за', (time_end - time_start))
    if error:
        save_file('error.txt', name_audio)


# Загрузка
def download(v_id):

    os.chdir(path)
    song = 0
    time_start = datetime.datetime.now()
    print('Начало загрузки', datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
    print('Путь загрузки:', path)
    print('vk_audio:', vk_audio.get(owner_id=v_id))

    for i in vk_audio.get(owner_id=v_id):
        try:
            song += 1
            r = requests.get(i['url'], stream=True)
            if 'Content-Length' not in r.headers:
                print('NET Content-Length | ', song)
                continue
            size = int(r.headers['Content-Length'])
            if r.status_code == 200:
                with open(str(song) + '_' + i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as file:
                    print('Загрузка:', i['artist'] + ' - ' + i['title'])
                    time.sleep(0.5)
                    for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size / 1024, unit='KB',
                                     leave=True):
                        file.write(data)
        except OSError:
            print('Ошибка загрузки:', song, i['artist'] + ' - ' + i['title'])

    time_end = datetime.datetime.now()
    print('Загружено', len(next(os.walk(path))[2]), 'песен за', (time_end - time_start))


if __name__ == "__main__":

    result = load_playlist()
    x = 1

    try:
        vk_session = vk_api.VkApi(login=login, password=password)
        vk_session.auth()
        print('Авторизация')
        vk = vk_session.get_api()
        vk_audio = audio.VkAudio(vk_session)
        print('Успех')

        for audio in result['result']['history']:
            print(f"{x} >>>>>>>>>>>>>>>>>>>>>>>>> {audio['id']} | {audio['artist']} - {audio['song']}")
            x += 1
            search(f"{audio['artist']} - {audio['song']}")

    except vk_api.AuthError:
        print('Неверный логин или пароль')

