import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.api.types import is_object_dtype
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

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

def ICAnalysis(data, ref):
    #the same, select numerical columns (an what I aim to separate?)
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != ref:
                cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)

    n_components = int(input('How many components you want?'))
    ica = FastICA(n_components=n_components, random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ICs  = pd.DataFrame(x_ica, columns=['IC1', 'IC2'])
    result  = pd.concat([target, ICs], axis=1)

    Plotter(result, 'ICA - Independent Components Analysis')

def TSNEanalysis(data, ref):
    ncomps = 2
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    for col in data.columns:
        if is_object_dtype(data[col]):
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.fillna(data.mean(numeric_only=True))
    tsne = TSNE(n_components=ncomps, random_state=42)
    embedded = tsne.fit_transform(data)

    plt.figure(figsize=(8,6))
    plt.scatter(embedded[:,0], embedded[:,1], s=20, cmap='viridis')
    plt.title('t-SNE Embedding')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.savefig('tsne_plot.png', dpi=300, bbox_inches='tight')



