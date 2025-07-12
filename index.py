import sys
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def read_file_data():
    try:
        df = pd.read_csv("NBA_2324_players.csv")
        print(dt)
        return df, True
    except:
        return None, False

if __name__ == "__main__":
    data, res = read_file_data()

    if res == False:
        print("data was not obtained")
        sys.exit(0)
    n = 2
    svd_solver = 'arpack'
    pca = PCA(n_components=n)
    itself = pca.fit(data)
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)

    reduced_self = pca.fir_transform(input_data)
