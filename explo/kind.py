
from explo.exploratories import correlation_matrix, boxplots, histograms, categoricals, dispersions
from abss.fs import current_project
from abss.data_setter import get_data

def ExploratoryAnalysis(cmd):
    datapath = current_project(['datapath', 'src'])
    res, data = get_data(datapath, ',')
    MSG = ''
    if cmd.all == True:
        msg = correlation_matrix(data)
        MSG = '{}\n{}'.format(MSG, msg)
        msg = categoricals(data)
        MSG = '{}\n{}'.format(MSG, msg)
        msg = boxplots(data)
        MSG = '{}\n{}'.format(MSG, msg)
        msg = histograms(data)
        MSG = '{}\n{}'.format(MSG, msg)
        msg = dispersions(data)
        MSG = '{}\n{}'.format(MSG, msg)
        return True, MSG
    else:
        msg = ''
        if cmd.corr_matrix == True:
            msg = correlation_matrix(data)
        else:
            msg = '----correlation matrix: not required'
        MSG = '{}\n{}'.format(MSG, msg)

        if cmd.histo == True:
            msg = histograms(data)
            MSG = '{}\n{}'.format(MSG, msg)
        else:
            MSG = '{}\n{}'.format(MSG, '----histogram: not required')
        
        if cmd.boxplot == True:
            msg = boxplots(data)
            MSG = '{}\n{}'.format(MSG, msg)
        else:
            MSG = '{}\n{}'.format(MSG, '----boxplot: not required')

        if cmd.categorics == True:
            msg = categoricals(data)
            MSG = '{}\n{}'.format(MSG, msg)
        else:
            MSG = '{}\n{}'.format(MSG, '----boxplot: not required')

        if cmd.dispersion == True:
            msg = dispersions(data)
            MSG = '{}\n{}'.format(MSG, msg)
        else:
            MSG = '{}\n{}'.format(MSG, '----boxplot: not required')

    return True, MSG

