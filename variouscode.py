 song = sp.audio_analysis(tracks['items'][0]['id'])

 import spotipy
    ...: from spotipy.oauth2 import SpotifyClientCredentials
    ...:
    ...: client_credentials_manager = SpotifyClientCredentials()
    ...: sp = spotipy.Spotify(client_credentials_manager=client_credentials_mana
    ...: ger)
    ...:
    ...: playlists = sp.user_playlists('spotify') #will list lots of playlists
    ...: while playlists:
    ...:     for i, playlist in enumerate(playlists['items']):
    ...:         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri
    ...: '],  playlist['name']))
    ...:     if playlists['next']:
    ...:         playlists = sp.next(playlists)
    ...:     else:
    ...:         playlists = None
    ...:

sp.search(tracks['items'][0]['name'], type='track')

import spotipy
    ...:
    ...: sp = spotipy.Spotify()
    ...: sp.trace = False
    ...:
    ...: # find album by name
    ...: album = "Pestbringer"
    ...: results = sp.search(q = "album:" + album, type = "album")
    ...:
    ...: # get the first album uri
    ...: album_id = results['albums']['items'][0]['uri']
    ...:
    ...: # get album tracks
    ...: tracks = sp.album_tracks(album_id)
    ...:
