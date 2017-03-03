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


def createdb(baseart):
    first = {'name': baseart.name, 'uri' : baseart.uri, 'followers': baseart.followers, 'genres': baseart.genres, 'popularity': baseart.popularity}
    tab.insert_one(first)
    for similar in baseart.relatedid:
        a = Artist(similar)
        next_artist = {'name': a.name, 'uri' : a.uri, 'followers': a.followers, 'genres': a.genres, 'type': a.type, 'popularity': a.popularity}
        tab.insert_one(next_artist)

def uris_base():
    return [doc['uri'].encode('utf-8') for doc in tab.find()]

def collect_uris(init_uris):
    uris_dump = set(init_uris)
    update_list = []
    for i in uris_dump:
        a = Artist(i)
        update_list.extend([ _ for _ in a.relatedid])
    uris_dump.update(update_list)
    print 'uri current length:', len(uris_dump)
    return uris_dump

def get_mainstream_uris(artistname):
    url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(artistname)
    res = requests.get(url)
    #return res['artists']['items'][0]['uri'].encode('utf-8')
    return res.json()['artists']['items'][0]['uri'].encode('utf-8')

def mainstream_uris_db(mainstream_uri):
    a = Artist(mainstream_uri)
    init_uris = a.relatedid
    uri_db = collect_uris(init_uris)
    uri_db_final = collect_uris(uri_db)
    return uri_db_final

# def genres_split(df):
#     genres = set()
#     for m in df.genres:
#         genres.update(g for g in m.split(','))
#         genres = sorted(genres)
    # for genre in genres:
    #     data[genre] = [genre in movie.split('|') for movie in data.genres]


if __name__ == '__main__':
    #RHCP database addition
    init_rhcp_uri = 'spotify:artist:0L8ExT028jH3ddEcZwqJJ5'
    baseart = Artist(init_rhcp_uri)
    # init_uris = uris_base()
    # uris_rhcp = collect_uris(init_uris)
    # uris_iter = collect_uris(uris_rhcp)
    # uris_rhcp.update(uris_iter)
    #getting mainstream cluster uris
    # mainstream = ['daft+punk', 'beyonce', 'the+beatles', 'kendrick+lamar', 'radiohead', 'luke+bryan']
    # mainstream2 = ['skrillex', 'led+zeppelin', 'adele', 'mumford+&+sons', '2pac', 'elton+john']
    # mainstream3 = ['taking+back+sunday', 'nelly', 'the+chainsmokers', 'ed+sheeran', 'carrie+underwood', 'lady+gaga', 'death+cab+for+cutie', 'bob+marley', 'outkast', 'spice+girls', 'amy+winehouse', 'michael+jackson']
    # mainstream4 = ['red+hot+chili+peppers', 'pitbull', 'eminem', 'a+tribe+called+quest', 'the+xx', 'miles+davis', 'jimi+hendrix', 'alabama+shakes', 'usher', 'tim+mcgraw', 'ace+of+base']
    # mainstream5 = ['deadmau5', 'kings+of+leon', 'drake', 'taylor+swift', 'arctic+monkeys', 'r.+kelly', 'dierks+bentley', 'britney+spears', 'fall+out+boy', 'enrique+iglesias', 'paramore', 'hozier']
    # midstream = ['spoon', 'lcd+soundsystem', 'sufjan+stevens', 'the+white+stripes', 'arcade+fire', 'erykah+badu', 'bon+iver', 'the+eagles', 'linkin+park', 'norah+jones', 'josh+groban', 'odesza']
    # midstream2 = ['tame+impala', 'chris+stapleton', 'my+morning+jacket', 'sturgill+simpson', 'ludacris', 'cake', 'beastie+boys', 'no+doubt', 'nine+inch+nails', 'disclosure', 'leon+bridges']
    # midstream3 = ['father+john+misty', 'porter+robinson', 'lorde', 'dj+khaled', 'bastille', 'gucci+mane', 'local+natives', 'mac+demarco', 'little+dragon', 'lettuce', 'easton corbin', 'a+tribe+called+quest', 'nine+inch+nails', 'beach+house', 'tool', 'phantogram', 'saint+motel', 'flume']
    # mainstream6 = ['the+lumineers', 'the+black+eyed+peas', 'kanye+west', 'kelly+clarkson', 'justin+bieber']
    mainstream7 = ['the+avett+brothers', 'metallica', 'bon+jovi', 'lil+wayne', 'mstrkrft', 'kehlani', 'tove+lo', 'bleachers', 'marshmello', 'cage+the+elephant', 'j+cole', 'major+lazer', 'm83', 'vic+mensa', 'daughter', 'cherub', 'ariana+grande', 'eric+church', 'chris+brown']
    res_list = []
    for i in mainstream7:
        res_list.append(get_mainstream_uris(i))
    #populate individual mainstream related dbs
    set_of_uris = set()
    for i in res_list:
        set_of_uris.update(mainstream_uris_db(i))
        print 'artist {} associated uris collected'.format(i)
        print 'total uri length', len(set_of_uris)
