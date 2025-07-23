import sys
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from .plotmaker import Plotter


def PCAnalysis(data, ref):
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != ref:
                cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
        
    rank = data.pop(ref)
    data.insert(0, ref, rank)
    rank = data.pop(ref)

    #data as features
    n_components = int(input('How many components you want?'))
    svd_solver = 'arpack'
    pcnames = []
    for i in range(n_components):
        i += 1
        pcnames.append(f"pc{i}")


    pca = PCA(n_components=n_components)
    pca.fit(data)
    pcs             = pca.transform(data) #principal components
    data_with_pcs   = pd.DataFrame(data=pcs,
                                columns=pcnames)
    complete = pd.concat([data_with_pcs, rank], axis=1)

    print(complete)
    variance = pca.explained_variance_ratio_
    print('Variance per principal components: ')
    for var, pcname in zip(variance, pcnames):
        print('{}: {}'.format(pcname, var))

    print('lost information by using {} components: '.format(len(variance)))
    print('-> {}'.format(1-np.sum(variance)))
    Plotter(complete, 'PCA - Principal Components Analysis')
