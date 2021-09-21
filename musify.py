import os
import re
import time

import requests, pickle
from bs4 import BeautifulSoup as Bs
import urllib.parse
from datetime import date
import json
from loguru import logger
from tqdm import tqdm

name_dir = 'mp3_musify'
path = r'D:\PycharmProjects\GOP_FM\\' + name_dir

if not os.path.exists(path):
    os.makedirs(path)

logger.add('logs/debug.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="DEBUG",
           rotation="1 MB", compression="zip")

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "Я:R"
                           "]+", flags=re.UNICODE)

def save_file(file, txt):
    try:
        with open(file, 'a') as f:
            f.write(txt + "\r")
    except:
        print("Ошибка записи в файл: ", file)

def search(name_audio):
    error = True
    session = requests.Session()
    params = {'searchText': name_audio}
    html = session.get('https://musify.club/search', params=urllib.parse.urlencode(params))
    try:
        soup = Bs(html.text, "lxml")
        div = soup.select_one('.playlist__item').select_one('.yaBrowser').attrs
        logger.debug("{}", div['download'])
    except:
        logger.error('NET audio')
        save_file('error.txt', name_audio)
        return False

    os.chdir(path)
    if not os.path.exists(emoji_pattern.sub(r'', div['download'])):
        r = requests.get("https://musify.club" + div['href'], stream=True)
        if 'Content-Length' not in r.headers:
            logger.error('NET Content-Length')
            error = True
        else:
            size = int(r.headers['Content-Length'])
            if r.status_code == 200:
                try:
                    with open(emoji_pattern.sub(r'', div['download']), 'wb') as file:
                        time.sleep(0.5)
                        error = False
                        save_file('good.txt', div['download'])
                        for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size / 1024, unit='KB',
                                         leave=True):
                            file.write(data)
                except:
                    logger.error('Не могу открыть файл: {}', emoji_pattern.sub(r'', div['download']))
                    error = True
            else:
                logger.error('error code {}', r.status_code)
                error = True
        if error:
            save_file('error.txt', name_audio)

def load_playlist():
    with open('playlist.txt', 'rb') as f:
        result = f.read()
        return json.loads(result)

if __name__ == "__main__":

    result = load_playlist()
    x = 1
    for audio in result['result']['history']:
        print(f"{x} >>>>>>>>>>>>>>>>>>>>>>>>> {audio['id']} | {audio['artist']} - {audio['song']}")
        x += 1
        search(f"{audio['artist']} - {audio['song']}")
