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
from abss.fs import write_csv

from abss.fs import current_project, take_n
from .plotmaker import Plotter

def data_separator(data, ref):
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    return data, target

def add(what, report):
    name = current_project(['project_name'])
    storypath = 'prs\{}\story.json'.format(name)
    current = {}
    with open(storypath, 'r') as file:
        current = json.load(file)
        current[what].append(report)

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
    n = take_n('methods', 'pca')
    files = {
        'pca_basic_chart_pcn': 'pca_{}_basic_pcn.png'.format(n),
        'pca_pcs':'pca_{}_pcs.csv'.format(n),
    }
    REPORT = {
        'method': 'pca',
        'n':n,
        'time': time,
        'lost_information':lost_information,
        'variance_ratio':variance_ratio.tolist(),
        'outputs': files,
    }
    Plotter(complete, 'PCA - Principal Components Analysis', files['pca_basic_chart_pcn'], cmd.ref)
    res, msg = write_csv(data_with_pcs, files['pca_pcs'])
    print(msg)
    add('methods', REPORT)

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

    n = take_n('methods', 'ica')
    files = {
        'ica_basic_chart_icn': 'ica_{}_basic_icn.png'.format(n),
        'ica_ics':'ica_{}_ics.csv'.format(n),
    }
    Plotter(complete, 'ICA - Independent Components Analysis', files['ica_basic_chart_icn'], cmd.ref)
    res, msg = write_csv(files['ica_ics'])
    print(msg)
    REPORT = {
        'method': 'ica',
        'n':n,
        'time': time,
        'comps':comps,
        'mixin':mixin,
        'meann':meann,
        'white':white,
        'outputs': files,
    }
    add('methods', REPORT)

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
    tsnes   = pd.DataFrame(x_tsne, columns=tsnenames)
    complete= pd.concat([tsnes, target], axis=1)

    n = take_n('methods', 'tsne')
    files = {
        'tsne_basic_chart_comps': 'tsne_{}_basic_comps.png'.format(n),
        'tsne_comps':'tsne_{}_comps.csv'.format(n),
    }
    Plotter(complete, 'tSNE Analysis', files['tsne_basic_chart_comps'], cmd.ref)
    res, msg = write_csv(tsnes, files['tsne_comps'])
    print(msg)
    REPORT = {
        'method':'tsne',
        'n':n,
        'time': time,
        'outputs': files,
    }
    add('methods', REPORT)


