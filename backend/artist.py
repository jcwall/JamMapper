import spotipy
import requests

class Artist:
    def __init__(self, artistid):
        url = 'https://api.spotify.com/v1/artists/{}'.format(artistid)
        artist = requests.get(url).json()
        self.id = artist['id'].encode('utf-8')
        self.uri = artist['uri'].encode('utf-8')
        self.name = artist['name'].encode('utf-8')
        self.genres = [genre.encode('utf-8') for genre in artist['genres']]
        self.followers = artist['followers']['total']#.astype(str)
        url2 = url = 'https://api.spotify.com/v1/artists/{}/related-artists'.format(self.id)
        simartists = requests.get(url2).json()['artists']
        self.related = [artist['name'].encode('utf-8') for artist in simartists]
        self.relatedid = [artist['id'].encode('utf-8') for artist in simartists]
        self.relateduri = [artist['uri'].encode('utf-8') for artist in simartists]
        self.popularity = artist['popularity']
