import json
import requests

def save_playlist():
    url = 'https://radiorecord.ru/api/api/station/history/?full&id=556'
    r = requests.get(url)
    print(r.status_code)
    with open('playlist.txt', 'wb') as f:
        f.write(r.content)

    return json.loads(r.content)

def load_playlist():
    with open('playlist.txt', 'rb') as f:
        result = f.read()
        return json.loads(result)


if __name__ == "__main__":

    result = save_playlist()
    #result = load_playlist()
    x = 1
    for audio in result['result']['history']:
        print(f"{x} >> {audio['id']} | {audio['artist']} - {audio['song']}")
        x += 1
