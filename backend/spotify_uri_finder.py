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
import eventful
import os
api = eventful.API(os.environ["EVENTFUL_ID"])

def get_uris(artistname):
    print artistname
    uris = []
    try:
        artists = artistname.split(',')
        uris = []
        for i in artists:
            url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(i)
            res1 = requests.get(url)
            uris.append(res1.json()['artists']['items'][0]['uri'].encode('utf-8'))
        return uris
    except (IndexError, ValueError, KeyError) as err:
        print 'ERROR!!!!!', err
        pass

def uri_finder(artist):
    url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(artist)
    res1 = requests.get(url)
    return res1.json()['artists']['items'][0]['uri'].encode('utf-8')


def clean_nones(show):
    if show[0] is not None:
        uris = show[0]
    if show[0] is None:
        uris = []
        artists = show[1].replace('with', ',').replace(':', ',').replace('-', ',').replace('w/', ',').replace('@', ',').replace('&', ',').replace('ft.', ',').replace('RE:', ',').replace('+', ',').replace('presents', ',').replace('feat.', ',').replace('**SOLD OUT**', ',').replace('/', ',').replace('***FREE SHOW***', ',').replace('(16+ Event)', ',').replace('featuring', ',').replace('(', ',').replace('(18+ event)', ',').replace('y', ',').split(',')
        for artist in artists:
            try:
                uri = uri_finder(artist)
                uris.append(uri)
            except (IndexError, ValueError, KeyError) as err:
                pass
    return uris

if __name__ == '__main__':
    with open('../pickle_jar/shows_master_list.pkl', 'r') as f:
        shows_master_list = pickle.load(f)
    uris_master_list = []
    for venue in shows_master_list:
        print '---------venue {} starting----------'.format(venue[0])
        venue_list = []
        for show in venue[1]:
            venue_list.append((get_uris(show[0]), show[0], show[1], show[2]))
        print '---------venue {} ending-------------'.format(venue[0])
        uris_master_list.append((venue[0], venue_list))
    final_list = []
    for venue in uris_master_list:
        print 'cleaning venue: {}'.format(venue[0])
        venue_list = []
        for show in venue[1]:
            venue_list.append((clean_nones(show), show[1], show[2], show[3]))
        final_list.append((venue[0], venue_list))
    with open('../pickle_jar/uris_master_list1.pkl', 'w') as f:
        pickle.dump(final_list, f)
