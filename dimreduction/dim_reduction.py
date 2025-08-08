import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from pandas.api.types import is_object_dtype
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from abss.fs import currentProject
from .plotmaker import Plotter

def data_separator(data, ref):
    print('ref: ', ref)
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
    current = {}
    with open(storypath, 'r') as file:
        current = json.load(file)
        current['methods'].append(report)

    with open(storypath, 'w') as file:
        json.dump(current, file, indent=4)

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
    time = str(datetime.now())

    projectname = currentProject('project_name')
    chartpath   = 'prs\{}\outputs\{}'.format(projectname,cmd.output)
    REPORT = {
        'method': 'pca',
        'time': time,
        'lost_information':lost_information,
        'variance_ratio':variance_ratio.tolist(),
        'pca_chart_path':chartpath,
    }
    Plotter(complete, 'PCA - Principal Components Analysis', chartpath, cmd.ref)
    add_method(REPORT)

def ICAnalysis(data, cmd):
    data, target = data_separator(data, cmd.ref)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)

    icnames = []
    for i in range(cmd.ncomps):
        i += 1
        icnames.append(f"ic{i}")
    ica = FastICA(n_components=cmd.ncomps, random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ics  = pd.DataFrame(x_ica, columns=icnames)
    complete  = pd.concat([ics, target], axis=1)

    comps = ica.components_.tolist()
    mixin = ica.mixing_.tolist()
    meann = ica.mean_.tolist()
    white = ica.whitening_.tolist()
    time = str(datetime.now())

    projectname = currentProject('project_name')
    chartpath   = 'prs\{}\outputs\{}'.format(projectname,cmd.output)
    Plotter(complete, 'ICA - Independent Components Analysis', chartpath, cmd.ref)
    REPORT = {
        'method': 'ica',
        'time': time,
        'chartpath':chartpath,
        'comps':comps,
        'mixin':mixin,
        'meann':meann,
        'white':white,
    }
    add_method(REPORT)

def TSNEanalysis(data, cmd):
    data, target = data_separator(data, cmd.ref)
    for col in data.columns:
        if is_object_dtype(data[col]):
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.fillna(data.mean(numeric_only=True))
    tsne = TSNE(n_components=cmd.ncomps, random_state=42)
    x_tsne = tsne.fit_transform(data)
    time = str(datetime.now())

    tsnenames = []
    for i in range(cmd.ncomps):
        i += 1
        tsnenames.append(f"tsne{i}")
    tsnes  = pd.DataFrame(x_tsne, columns=tsnenames)
    complete  = pd.concat([tsnes, target], axis=1)

    projectname = currentProject('project_name')
    chartpath   = 'prs\{}\outputs\{}'.format(projectname, cmd.output)
    Plotter(complete, 'tSNE Analysis', chartpath, cmd.ref)
    REPORT = {
        'method':'tsne',
        'time': time,
        'chartpath':chartpath,
    }
    add_method(REPORT)




