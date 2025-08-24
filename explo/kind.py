
from explo.exploratories import correlation_matrix, boxplot, histogram, categoricals, dispersions
from abss.fs import current_project
from data_setter import get_data

def ExploratoryAnalysis(cmd):
    datapath = current_project(['datapath', 'src'])
    res, data = get_data(datapath)
    MSG = ''
    if cmd.all == True:
        msg = correlation_matrix(data)
        MSG = '{}\n{}'.format(MSG, msg)
        msg = categoricals(data)
        MSG = '{}\n{}'.format(MSG, msg)
        return True, MSG
    else:
        if cmd.corr_matrix == True:
            msg = correlation_matrix()
            MSG = '{}'.format(MSG, msg)
        else:
            MSG = '{}'.format(MSG, '----correlation matrix: not required')

        if cmd.histo == True:
            msg = make_histogram()
            MSG = '{}'.format(MSG, msg)
        else:
            MSG = '{}'.format(MSG, '----histogram: not required')
        
        if cmd.boxplot == True:
            msg = boxplot()
            MSG = '{}'.format(MSG, msg)
        else:
            MSG = '{}'.format(MSG, '----boxplot: not required')

        if cmd.categorics == True:
            msg = categoricals()
            MSG = '{}'.format(MSG, msg)
        else:
            MSG = '{}'.format(MSG, '----boxplot: not required')

        if cmd.dispersion == True:
            msg = dispersions()
            MSG = '{}'.format(MSG, msg)
        else:
            MSG = '{}'.format(MSG, '----boxplot: not required')

    return True, MSG

