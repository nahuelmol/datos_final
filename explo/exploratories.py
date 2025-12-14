
import matplotlib.pyplot as plt
import numpy as np

from abss.story import add
from abss.fs import take_n, current_project
from abss.data_setter import get_data

from datetime import datetime
from explo.plots import Plot

def does_exists(ref):
    datapath= current_project(['datapath', 'src'])
    res, data    = get_data(datapath, ',')
    if res == True:
        if ref in data.columns.tolist():
            return True
    return False

def correlation_matrix(df):
    n = take_n('exploratory_analysis', 'corr_matrix')
    files = {
        'corr_matrix_plot': 'corr_matrix_{}.png'.format(n),
    }
    REPORT = {
        'metric': 'corr_matrix',
        'n':n,
        'time':str(datetime.now()),
        'outputs': files,
    }
    PLOT = Plot(files['corr_matrix_plot'], df)
    res  = PLOT.corr_plot()
    if res == True:
        add('exploratory_analysis', REPORT)
        return '----correlation matrix:done!'
    else:
        return '----correlation matrix:failed!'


def categoricals(data):
    cat_cols = data.select_dtypes(['object', 'category']).columns.tolist()
    if (len(cat_cols) == 0):
        print('no categorical variables')
        return '---categoricals: not posible'
    else:
        listed = ''
        for i in cat_cols:
            listed = '{} {}'.format(i, listed)
        print('categorical variables: {}'.format(listed))

    ref = ''
    if(current_project(['global', 'var']) != None):
        ref = current_project(['global', 'var'])
    else:
        print('global - var does not exists')
        ref = input('insert categorical now: ')

    n = take_n('exploratory_analysis', 'categos')
    files = {
        'categorical_plot': 'categorical_{}.png'.format(n),
    }
    REPORT = {
        'metric': 'categos',
        'n':n,
        'time':str(datetime.now()),
        'outputs': files,
    }
    PLOT = Plot(files['categorical_plot'], data[ref])
    res  = PLOT.hist()
    if res == True:
        add('exploratory_analysis', REPORT)
        return '----categorical view:done!'
    else:
        return '----categorical view:failed!'

def dispersions(data):
    ref = ''
    if(current_project(['global', 'hvar']) != None):
        ref = current_project(['global', 'hvar'])
    else:
        print('dispersions: var does not exists')
        ref = input('dispersions: insert variable now: ')
    var = data[ref].var()
    std = data[ref].std()
    mea = data[ref].mean()
    range_ = data[ref].max() - data[ref].min()
    var_coeff = std / mea

    REPORT = {
        'metric':'dispersion',
        'time':str(datetime.now()),
        'ref':ref,
        'variance':var,
        'deviation':std,
        'mean':mea,
        'range':range_,
        'variation_coefficient':var_coeff,
        'outputs':{},
    }
    add('exploratory_analysis', REPORT)
    return '----dispersions: done!'

def histograms(data):
    ref = ''
    if(current_project(['global', 'hvar']) != None):
        ref = current_project(['global', 'hvar'])
    else:
        print('histogram: var does not exists')
        ref = input('histogram: insert variable now: ')
    n = take_n('exploratory_analysis', 'histos')
    files   = {
        'histo':'histo_{}.png'.format(n),
        'histo_kde':'histo_{}_kde.png'.format(n),
        'histo_kde_shade':'histo_{}_kde_shade.png'.format(n),
    }
    PLOT = Plot(files['histo'], data)
    PLOT = Plot(files['histo_kde'], data)
    PLOT = Plot(files['histo_kde_shade'], data)
    PLOT.histos(ref, False)
    PLOT.histos(ref, True)
    PLOT.histos(ref, False)

    REPORT  = {
        'metric':'histos',
        'n':n,
        'time':str(datetime.now()),
        'outputs':files,
    }
    add('exploratory_analysis', REPORT) 
    return '----histograms:done!'

def boxplots(data):
    ref = ''
    if(current_project(['global', 'hvar']) != None):
        ref = current_project(['global', 'hvar'])
    else:
        print('boxlplots: var does not exists')
        ref = input('boxplots: insert variable now: ')
        if not does_exists(ref):
            return '----boxplots:variable not exists'
    n = take_n('exploratory_analysis', 'boxplots')
    files = {
        'boxplot_basic':'boxplot_{}_basic.png'.format(n)
    }
    REPORT = {
        'metric':'boxplot',
        'n':n,
        'time':str(datetime.now()),
        'outputs':files,
    }
    PLOT = Plot(files['boxplot_basic'], data[ref])
    PLOT.boxplot()
    add('exploratory_analysis', REPORT)
    return '----boxplots:done!'
