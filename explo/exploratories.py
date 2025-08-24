
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from abss.story import add
from abss.fs import take_n, current_project
from datetime import datetime

def plot_hist(filename):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    return True

def plot(corr_matrix, filename):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    plt.figure(figsize=(12,8))
    sns.heatmap(corr_matrix, cmap='coolwarm', mask=mask)
    plt.title(f"Correlation Matrix", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(filepath, dpi=300)
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
    print('categorical variables: {}'.format(cat_cols.tolist()))

    res = input('insert or take from global var? (i\\t)')
    ref = ''

    if(res == 'i'):
        ref = input('insert it: ')
    elif(res == 't'):
        if(current_project(['global', 'var']) != None):
            ref = current_project(['global', 'var'])
        else:
            print('global - var does not exists')
            ref = input('insert categorical now: ')

    sns.countplot(x=data[ref])
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
    res = plot_hist(files['categorical_plot'])
    if res == True:
        add('exploratory_analysis', REPORT)
        return '----categorical view:done!'
    else:
        return '----categorical view:failed!'

def dispersions(data):
    ref = input('insert variable')
    var = data[ref].var()
    std = data[ref].std()
    mea = data[ref].mean()
    range_ = data[ref].max() - data[ref].min
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
    }

def histogram(data):
    sns.histplot(data, kde=False, bins=20)
    plt.savefig('histo.png')
    sns.histplot(data, kde=True, bins=20)
    plt.savefig('histo_kde.png')
    sns.kdeplot(data, shade=True)
    plt.savefig('histo_kde_shade.png')

def boxplot(data):
    ref = input("insert ref: ")
    sns.boxplot(x=data[ref])
    plt.savefig('boxplot.png')



