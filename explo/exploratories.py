
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from abss.story import add
from abss.fs import take_n, current_project
from datetime import datetime

def does_exists(ref):
    datapath= current_project(['datapath', 'src'])
    data    = get_data(datapath)
    if ref in data.columns.tolist():
        return True
    return False

def plt_boxplot(X, filename):
    pname = current_project(['project_name'])
    fpath = 'prs\{}\outputs\{}'.format(pname, filename)
    sns.boxplot(x=X)
    plt.savefig(fpath, dpi=300)
    plt.close()

def plot_histos(data, x, kde, filename):
    data = data.select_dtypes(include=['number'])
    pname = current_project(['project_name'])
    fpath = 'prs\{}\outputs\{}'.format(pname, filename)
    sns.histplot(data=data, x=x, kde=kde, bins=20)
    plt.savefig(fpath, dpi=300)
    plt.close()

def plot_hist(X, filename):
    sns.countplot(x=X)
    pname = current_project(['project_name'])
    fpath = 'prs\{}\outputs\{}'.format(pname, filename)
    plt.savefig(fpath, dpi=300)
    plt.close()
    return True

def plot(corr_matrix, filename):
    pname = current_project(['project_name'])
    fpath = 'prs\{}\outputs\{}'.format(pname, filename)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    plt.figure(figsize=(12,8))
    sns.heatmap(corr_matrix, cmap='coolwarm', mask=mask)
    plt.title(f"Correlation Matrix", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(fpath, dpi=300)
    plt.close()
    return True

def correlation_matrix(df):
    numerical = df.select_dtypes(include=['number']).copy()
    corr_matrix = numerical.corr()

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
    res = plot(corr_matrix, files['corr_matrix_plot'])
    if res == True:
        add('exploratory_analysis', REPORT)
        return '----correlation matrix:done!'
    else:
        return '----correlation matrix:failed!'


def categoricals(data):
    cat_cols = data.select_dtypes(['object', 'category']).columns
    cols_len = len(cat_cols.list())
    if cols_len == 0:
        print('no categorical variables')
        return '---categoricals: not posible'
    else:
        print('categorical variables: {}'.format(cat_cols.tolist()))

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
    res = plot_hist(data[ref], files['categorical_plot'])
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
    plot_histos(data, ref, False, files['histo'])
    plot_histos(data, ref, True,  files['histo_kde'])
    plot_histos(data, ref, False, files['histo_kde_shade'])
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
    plt_boxplot(data[ref], files['boxplot_basic'])
    add('exploratory_analysis', REPORT)
    return '----boxplots:done!'
