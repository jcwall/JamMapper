import spotipy
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client['spotifydb']
tab = db['artist_list']
from artist import Artist
import requests
import pickle
import more_itertools

def mongo_pop(set_of_uris):
    for uri in set_of_uris:
        a = Artist(uri)
        next_artist = {'name': a.name, 'uri' : a.uri, 'followers': a.followers, 'genres': a.genres, 'type': a.type, 'popularity': a.popularity}
        tab.insert_one(next_artist)

def prep_uris(upcoming_shows):
    strictly_uris = []
    for venue in upcoming_shows:
        for show in venue[1]:
            strictly_uris.append(show[0])
    return list(more_itertools.flatten(strictly_uris))

def test_pop(coming_soon):
    for uri in coming_soon:
        a = Artist(uri)
        print a.name, a.uri

if __name__ == '__main__':
    txt_dumps = ['../pickle_jar/uri_dump9.txt', '../pickle_jar/uri_dump10.txt']
    master_list = set()
    for txt in txt_dumps:
        with open(txt, 'rb') as f:
            master_list.update(pickle.load(f))
    master_list = list(master_list)
    print 'now populating mongodb!'
    mongo_pop(master_list)
    # with open('../pickle_jar/uris_final_list2.txt', 'r') as f:
    #     upcoming_uris = pickle.load(f)
    # coming_soon = prep_uris(upcoming_uris)
    # # test_pop(coming_soon)
    # upcoming = set(coming_soon)
    # mongo_pop(upcoming)
