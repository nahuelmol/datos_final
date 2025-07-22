import sys
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def get_data():
    try:
        df = pd.read_csv("NBA_2324_players.csv")
        return True, df
    except:
        return False, None

def graphPC(pcs):
    import matplotlib.pyplot as plt
    filapath = 'output.png'
    plt.figure(figsize=(8,6))
    plt.scatter(pcs[0], pcs[1], c='blue', cmap='viridis',
                egdecolor='k', s=50)
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.title('PCA analysis')
    plt.colorbar(scatter)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

def PcaApplication(data):
    features = data[['RPG', 'APG', 'SPG']]
    n_components = int(input('How many components you want?'))
    svd_solver = 'arpack'
    pcnames = []
    for i in range(n_components):
        pcnames.append(f"pc{i}")

    pca = PCA(n_components=n_components)
    pca.fit(features)
    pcs             = pca.transform(features) #principal components
    data_with_pcs   = pd.DataFrame(data=pcs,
                                columns=pcnames)
    complete = pd.concat([data_with_pcs, data['RANK']], axis=1)

    #graphPC(complete)


if __name__ == "__main__":
    res, data = get_data()
    if res == False:
        print("data was not obtained")
        sys.exit(0)
    cols_to_drop = ['TEAM', 'POS', 'NAME']
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
        
    rank = data.pop('RANK')
    data.insert(0, 'RANK', rank)
    PcaApplication(data)
