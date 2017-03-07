import pickle
import pandas as pd
import numpy as np





if __name__ == '__main__':
    with open('../pickle_jar/topten.txt', 'r') as f:
        topten = pickle.load(f)
    # with open('../pickle_jar/master.txt', 'r') as f:
    #     master = pickle.load(f)
    with open('../pickle_jar/df_fin.txt', 'r') as f:
        df_fin = pickle.load(f)


# rhcp = dist_mat[0].argsort()[:5]
#
# rhcp = dist_mat[0].argsort()[80:120]
#
# name_uri_df.loc[rhcp, :]
#
# gramatik = dist_mat[516].argsort()[:40]
#
# In [21]: name_uri_df.loc[gramatik, :]
#
# name_uri_df.loc[500:550, :]
