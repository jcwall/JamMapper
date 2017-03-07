import spotipy

class Artist:
    def __init__(self, artisturi):
        sp = spotipy.Spotify()
        artist = sp.artist(artisturi)
        self.id = artist['id'].encode('utf-8')
        self.uri = artist['uri'].encode('utf-8')
        self.name = artist['name'].encode('utf-8')
        self.genres = [genre.encode('utf-8') for genre in artist['genres']]
        self.followers = artist['followers']['total']#.astype(str)
        simartists = sp.artist_related_artists(artist['id'])
        self.related = [artist['name'].encode('utf-8') for artist in simartists['artists']]
        self.relatedid = [artist['uri'].encode('utf-8') for artist in simartists['artists']]
        self.popularity = artist['popularity']
        self.type = artist['type']
