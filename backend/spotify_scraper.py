import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client['spotifydb']
tab = db['artist_list']
from artist import Artist
import requests

def createdb(baseart):
    first = {'name': baseart.name, 'uri' : baseart.uri, 'followers': baseart.followers, 'genres': baseart.genres, 'popularity': baseart.popularity}
    tab.insert_one(first)
    for similar in baseart.relatedid:
        a = Artist(similar)
        next_artist = {'name': a.name, 'uri' : a.uri, 'followers': a.followers, 'genres': a.genres, 'type': a.type, 'popularity': a.popularity}
        tab.insert_one(next_artist)

def get_mainstream_ids(artist):
    url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(artist)
    res = requests.get(url).json()['artists']['items']
    searchresults = [i['id'] for i in res]
    return searchresults[0]

def mainstream_simartists(mainstream_id):
    a = Artist(mainstream_id)
    sim_ids = a.relatedid
    ids = set(sim_ids)
    for i in sim_ids:
        sim = Artist(i)
        ids.update([_ for _ in sim.relatedid])
    final_ids = set()
    for i in ids:
        sim = Artist(i)
        final_ids.update([_ for _ in sim.relateduri])
    return final_ids


if __name__ == '__main__':
    init_rhcp_uri = '0L8ExT028jH3ddEcZwqJJ5'
    #baseart = Artist(init_rhcp_uri)
    #createdb(baseart)
    # res_list = [get_mainstream_ids(artist) for artist in mainstream10]
    # set_of_uris = set()
    # for i in res_list:
    #     set_of_uris.update(mainstream_simartists(i))
