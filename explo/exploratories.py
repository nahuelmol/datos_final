
import matplotlib.pyplot as plt
import numpy as np

from abss.story import add
from abss.fs import taken, current_project
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

class Explorer:
    def __init__(self, data, cmd):
        self.data   = data
        self.cmd    = cmd
        self.MSG    = ''
        self.message = None

        if cmd.all == True:
            self.correlation_matrix(data)
            self.n = taken('exploratory_analysis', 'histos')
            self.REPORT['metric'] = 'histos'
            self.MSG = '{}\n{}'.format(self.MSG, self.message)

            self.categoricals(data)
            self.n = taken('exploratory_analysis', 'categos')
            self.REPORT['metric'] = 'categos'
            self.MSG = '{}\n{}'.format(self.MSG, self.message)

            self.boxplots(self.data)
            self.n = taken('exploratory_analysis', 'boxplot')
            self.REPORT['metric'] = 'boxplot'
            self.MSG = '{}\n{}'.format(self.MSG, self.message)

            self.histograms(self.data)
            self.n = taken('exploratory_analysis', 'histos')
            self.REPORT['metric'] = 'histos'
            self.MSG = '{}\n{}'.format(self.MSG, self.message)

            msg = dispersions(data)
            self.n = taken('exploratory_analysis', 'dispersion')
            self.REPORT['metric'] = 'dispersion'
            self.MSG = '{}\n{}'.format(self.MSG, self.message)
            return True, self.MSG
        else:

            if self.cmd.corr_matrix == True:
                self.correlation_matrix(self.data)
                self.n = taken('exploratory_analysis', 'corr_matrix')
                self.REPORT['metric'] = 'corr_matrix'
                self.MSG = '{}\n{}'.format(self.MSG, self.message)
            else:
                msg = '----correlation matrix: not required'

            if cmd.histo == True:
                self.histograms(data)
                self.n = taken('exploratory_analysis', 'histos')
                self.REPORT['metric'] = 'histos'
                self.MSG = '{}\n{}'.format(self.MSG, self.message)
            else:
                self.MSG = '{}\n{}'.format(self.MSG, '----histogram: not required')
            
            if cmd.boxplot == True:
                self.boxplots(self.data)
                self.n = taken('exploratory_analysis', 'boxplot')
                self.REPORT['metric'] = 'boxplot'
                self.MSG = '{}\n{}'.format(self.MSG, self.message)
            else:
                self.MSG = '{}\n{}'.format(self.MSG, '----boxplot: not required')

            if cmd.categorics == True:
                self.categoricals(self.data)
                self.n = taken('exploratory_analysis', 'categos')
                self.REPORT['metric'] = 'categos'
                self.MSG = '{}\n{}'.format(self.MSG, self.message)
            else:
                self.MSG = '{}\n{}'.format(MSG, '----categorical: not required')

            if cmd.dispersion == True:
                self.dispersions(self.data)
                self.n = taken('exploratory_analysis', 'dispersion')
                self.REPORT['metric'] = 'dispersion'
                self.MSG = '{}\n{}'.format(self.MSG, self.message)
            else:
                self.MSG = '{}\n{}'.format(self.MSG, '----dispersion: not required')

        self.REPORT['n']    = self.n
        self.REPORT['time'] = str(datetime.now()),

    def correlation_matrix(self):
        files = {
            'corr_matrix_plot': 'corr_matrix_{}.png'.format(self.n),
        }
        self.REPORT['outputs'] = files
        }
        PLOT = Plot(files['corr_matrix_plot'], df)
        res  = PLOT.corr_plot()
        if res == True:
            self.message = '----correlation matrix:done!'
        else:
            self.message = '----correlation matrix:failed!'

    def categoricals(self):
        cat_cols = data.select_dtypes(['object', 'category']).columns.tolist()
        if (len(cat_cols) == 0):
            print('no categorical variables')
            self.message = '---categoricals: not posible'
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

        files = {
            'categorical_plot': 'categorical_{}.png'.format(self.n),
        }
        self.REPORT['outputs'] = files
        PLOT = Plot(files['categorical_plot'], data[ref])
        res  = PLOT.hist()
        if res == True:
            self.message = '----categorical view:done!'
        else:
            self.message = '----categorical view:failed!'

    def dispersions(self):
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

        self.REPORT['variance'] = var
        self.REPORT['deviation'] = std
        self.REPORT['mean'] = mea
        self.REPORT['range'] = range_
        self.REPORT['variation_coefficient'] = var_coeff
        self.REPORT['outputs'] = {}
        self.message = '----dispersions: done!'

    def histograms(self):
        ref = ''
        if(current_project(['global', 'hvar']) != None):
            ref = current_project(['global', 'hvar'])
        else:
            print('histogram: var does not exists')
            ref = input('histogram: insert variable now: ')
        files   = {
            'histo':'histo_{}.png'.format(self.n),
            'histo_kde':'histo_{}_kde.png'.format(self.n),
            'histo_kde_shade':'histo_{}_kde_shade.png'.format(self.n),
        }
        PLOT = Plot(files['histo'], data)
        PLOT = Plot(files['histo_kde'], data)
        PLOT = Plot(files['histo_kde_shade'], data)
        PLOT.histos(ref, False)
        PLOT.histos(ref, True)
        PLOT.histos(ref, False)

        self.REPORT['outputs'] = files
        self.message = '----histograms:done!'

    def boxplots(self):
        ref = ''
        if(current_project(['global', 'hvar']) != None):
            ref = current_project(['global', 'hvar'])
        else:
            print('boxlplots: var does not exists')
            ref = input('boxplots: insert variable now: ')
            if not does_exists(ref):
                self.message = '----boxplots:variable not exists'
        files = {
            'boxplot_basic':'boxplot_{}_basic.png'.format(self.n)
        }
        self.REPORT['outputs'] = files
        PLOT = Plot(files['boxplot_basic'], data[ref])
        PLOT.boxplot()
        self.message = '----boxplots:done!'
