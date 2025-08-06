import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.api.types import is_object_dtype
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from abss.fs import currentProject
from .plotmaker import Plotter

def data_separator(data, ref):
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    return data, target

def add_method(report):
    name = ''
    with open('manifest.json', 'r') as file:
        name = json.load(file)['project_name']
    storypath = 'prs\{}\story.json'.format(name)
    new_meth  = json.dumps(str(report))
    with open(storypath, 'r') as file:
        current = json.load(file)
        current['methods'].append(new_meth)
    with open(storypath, 'w') as file:
        json.dump(current, file)

def PCAnalysis(data, cmd):
    data, target = data_separator(data, cmd.ref)
    pcnames = []
    for i in range(cmd.ncomps):
        i += 1
        pcnames.append(f"pc{i}")

    pca = PCA(n_components=cmd.ncomps)
    pca.fit(data)
    pcs             = pca.transform(data)
    data_with_pcs   = pd.DataFrame(data=pcs,
                                columns=pcnames)
    complete = pd.concat([data_with_pcs, target], axis=1)

    variance_ratio = pca.explained_variance_ratio_
    lost_information = (1-np.sum(variance_ratio))

    projectname = currentProject('project_name')
    chartpath   = 'prs\{}\outputs\{}'.format(projectname,cmd.output)
    REPORT = {
        'lost_information':lost_information,
        'variance_ratio':variance_ratio,
        'pca_chart_path':chartpath,
    }
    Plotter(complete, 'PCA - Principal Components Analysis', chartpath, cmd.ref)
    add_method(REPORT)

def ICAnalysis(data, cmd):
    data, target = data_separator(data, cmd.ref)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)

    ica = FastICA(n_components=cmd.ncomps, random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ICs  = pd.DataFrame(x_ica, columns=['IC1', 'IC2'])
    result  = pd.concat([target, ICs], axis=1)

    REPORT = {
        'result':result,
    }
    outputpath = 'prs\outputs\{}'.format(cmd.output)
    Plotter(result, 'ICA - Independent Components Analysis', outputpath, cmd.ref)

def TSNEanalysis(data, cmd):
    data, target = data_separator(data, cmd.ref)
    for col in data.columns:
        if is_object_dtype(data[col]):
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.fillna(data.mean(numeric_only=True))
    tsne = TSNE(n_components=cmd.ncomps, random_state=42)
    embedded = tsne.fit_transform(data)

    plt.figure(figsize=(8,6))
    plt.scatter(embedded[:,0], embedded[:,1], s=20, cmap='viridis')
    plt.title('t-SNE Embedding')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.savefig('tsne_plot.png', dpi=300, bbox_inches='tight')



