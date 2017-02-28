import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client['spotifydb']
tab = db['artist_list']
import pickle
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

def clean_df(df):
    df['genres'] = df['genres'].apply(lambda x: np.nan if len(x) == 0 else x)
    df.drop('type', axis=1, inplace=True)
    df['followers'] = df['followers'].replace(np.nan, 0)
    df.drop('_id', axis=1, inplace=True)
    df.loc[df['genres'].notnull(), 'genres'] = df.loc[df['genres'].notnull(), 'genres'].map(lambda x: '|'.join(x))
    genre_dummy = df['genres'].str.get_dummies()
    df = pd.concat([df, genre_dummy], axis=1)
    for col in ['followers', 'popularity']:
        df[col] = (df[col] - df[col].mean()) / (df[col].max() - df[col].min())
    return df

def add_venues(df):
    with open('uris_final_list.txt', 'r') as f:
        upcoming_uris = pickle.load(f)
    null_genres = df['genres'].isnull()
    artist_venue = {}
    for venue in upcoming_uris:
        v = venue[0]
        for show in venue[1]:
            for s in show[0]:
                artist_venue[s] = v
    df['venue'] = df['uri'].map(artist_venue)
    df.drop('genres', axis=1, inplace=True)
    return df, artist_venue

def more_features(df):
    venue_dummy = df['venue'].str.get_dummies()
    dfnew = pd.concat([df, venue_dummy], axis=1)
    dfnew.drop('venue', axis=1, inplace=True)
    return dfnew

def dist_matrix(df):
    name = df.pop('name')
    uri = df.pop('uri')
    data = df
    dist = pdist(df, 'cosine')
    dist_df = pd.DataFrame(squareform(dist), index=df.index, columns = df.index)
    name_uri_df = pd.concat([name, uri], axis=1)
    return dist_df, name_uri_df

# def same_bill(df):
#     df['same_bill'] = if artist are performing for same show

if __name__ == '__main__':
    df = (pd.DataFrame(list(tab.find()))).ix[3:]
    dfnew = clean_df(df.reset_index())
    df2, venues = add_venues(dfnew)
    df_final = more_features(df2)
    dist_mat, name_uri_df = dist_matrix(df_final)
    with open('dist_mat.txt', 'w') as f:
        pickle.dump(dist_mat, f)
    with open('name_uri_df.txt', 'w') as f:
        pickle.dump(name_uri_df, f)
