if __name__ == '__main__':
    with open('dist_mat.txt', 'r') as f:
        dist_mat = pickle.load(f)
    with open('name_uri_df.txt', 'r') as f:
        name_uri_df = pickle.load(f)


rhcp = dist_mat[0].argsort()[:5]

rhcp = dist_mat[0].argsort()[80:120]

name_uri_df.loc[rhcp, :]

gramatik = dist_mat[516].argsort()[:40]

In [21]: name_uri_df.loc[gramatik, :]

name_uri_df.loc[500:550, :]
