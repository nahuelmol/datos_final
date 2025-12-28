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

from abss.fs import current_project, taken
from .plotmaker import Plotter
from abss.story import add

def data_separator(data, ref):
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    return data, target

class Reductor:
    def __init__(self, data, cmd):
        self.data   = data
        self.ref    = cmd.ref
        self.data, self.target = data_separator(self.data, cmd.ref)
        self.cmp_names = []
        for i in range(cmd.ncomps):
            i += 1
            self.cmp_names.append(f"{cmd.method}_cmp{i}")
        
        self.ncomps         = cmd.ncomps
        self.REPORT['time'] = str(datetime.now())
        self.REPORT['n']    = taken('methods', cmd.method)
        
        self.cmps       = None
        self.complete   = None
        self.pcs        = None
        self.ics        = None
        self.tsnes      = None
        self.transform  = None  

        if(cmd.method == 'pca'):
            self.PCAnalysis()
        elif (cmd.method = 'ica'):
            self.ICAnalysis()
        elif (cmd.method = 'tsnes'):
            self.TSNEanalysis()
        else:
            print('not recognized method')

    def build(self):
        self.transform  = self.cmps.transform(self.data)
        data_with_cmps  = pd.DataFrame(data=self.pcs, columns=self.cmp_names)
        self.complete   = pd.concat([data_with_pcs, self.target], axis=1)
        Plotter(self.complete, self.plot_name, self.file_plot_name, self.ref)
        res, msg = write_csv(data_with_cmps, self.file_data_name)

    def PCAnalysis(self):
        self.cmps       = PCA(n_components=self.ncomps)
        self.cmps.fit(self.data)

        variance_ratio = self.cmps.explained_variance_ratio_
        lost_information = (1-np.sum(variance_ratio))
        files = {
            'pca_basic_chart_pcn': 'pca_{}_basic_pcn.png'.format(n),
            'pca_pcs':'pca_{}_pcs.csv'.format(n),
        }
        self.REPORT['lost_information'] = lost_information
        self.REPORT['variance_ratio']   = variance_ratio.tolist()
        self.REPORT['outputs']          = files
        self.plot_name                  = 'PCA - Principal Components Analysis'
        self.file_plot_name             = files['pca_basic_chart_pcn']
        self.file_data_name             = files['pca_pcs']

    def ICAnalysis(data, cmd):
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(self.data)

        self.cmps       = FastICA(n_components=self.ncomps, random_state=0)
        self.ics        = ica.fit_transform(x_scaled)
        data_with_ics   = pd.DataFrame(self.ics, columns=self.cmp_names)
        self.complete   = pd.concat([data_with_ics, self.target], axis=1)

        comps = self.cmps.components_.tolist()
        mixin = self.cmps.mixing_.tolist()
        meann = self.cmps.mean_.tolist()
        white = self.cmps.whitening_.tolist()

        files = {
            'ica_basic_chart_icn': 'ica_{}_basic_icn.png'.format(n),
            'ica_ics':'ica_{}_ics.csv'.format(n),
        }
        self.REPORT['comps'] = comps
        self.REPORT['mixin'] = mixin
        self.REPORT['meann'] = meann
        self.REPORT['white'] = white,
        self.REPORT['outputs'] = files

    def TSNEanalysis(self):
        for col in self.data.columns:
            if is_object_dtype(self.data[col]):
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
        self.data = self.data.fillna(self.data.mean(numeric_only=True))

        self.cmps       = TSNE(n_components=cmd.ncomps, random_state=42)
        self.tsnes      = tsne.fit_transform(data)
        data_with_tsnes = pd.DataFrame(self.tsnes, columns=tsnenames)
        self.complete   = pd.concat([data_with_tsnes, self.target], axis=1)

        files = {
            'tsne_basic_chart_comps': 'tsne_{}_basic_comps.png'.format(n),
            'tsne_comps':'tsne_{}_comps.csv'.format(n),
        }
        self.REPORT['outputs'] = files

