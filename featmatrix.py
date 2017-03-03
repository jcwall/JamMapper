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
        df[col] = df[col]/df[col].max()
    df.drop_duplicates(subset='name', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def add_venues(df):
    with open('../pickle_jar/uris_final_list.txt', 'r') as f:
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
    # dfnew.drop('venue', axis=1, inplace=True)
    return dfnew

def dist_matrix(df):
    df2 = df.copy()
    live_only = df2.loc[df2['venue'].notnull(), :]
    name = df.pop('name')
    uri = df.pop('uri')
    venue = df.pop('venue')
    data = df
    dist = pdist(df, 'cosine')
    master = pd.DataFrame(squareform(dist), index=df.index, columns = df.index)
    #master = pd.concat([dist_df, name, uri, venue], axis=1)
    return master

def top_ten(master,df):
    top10_performing = {}
    live_only = df.loc[df2['venue'].notnull(), :]
    #for index, row in master.iterrows():
    for i in master.columns:
        band = master.loc[i, :]
        mask = np.in1d(np.argsort(band.values), live_only.index)
        top_ten = np.argsort(band.values)[mask][:10]
        top10_performing[df2.loc[i, 'uri']] = top_ten
    return top10_performing

# def same_bill(df):
#     df['same_bill'] = if artist are performing for same show

if __name__ == '__main__':
    df = (pd.DataFrame(list(tab.find())))
    dfnew = clean_df(df)
    print dfnew.columns
    print dfnew.head(5)
    df2, venues = add_venues(dfnew)
    df_final = more_features(df2)
    df_final2 = df_final.copy()
    master = dist_matrix(df_final)
    #top10_performing = top_ten(master, df_final2)


    # with open('../pickle_jar/top20_performing.txt', 'w') as f:
    #     pickle.dump(top20_performing, f)
    # with open('../pickle_jar/df_final.txt', 'w') as f:
    #     pickle.dump(df_final, f)
    # with open('dist_mat.txt', 'w') as f:
    #     pickle.dump(dist_mat, f)
    # with open('name_uri_df.txt', 'w') as f:
    #     pickle.dump(name_uri_df, f)
