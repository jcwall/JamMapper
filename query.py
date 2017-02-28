import requests
import bs4
from artist import Artist

def starter_uris():
    url = 'https://api.spotify.com/v1/artists/6vWDO969PvNqNYHIOW5v0m/related-artists'
    r = requests.get(url).json()
    uris = [i['uri'].encode('utf-8') for i in r['artists']]
    return uris

if __name__ == '__main__':
    uris = starter_uris()
