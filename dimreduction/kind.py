import sys

from dimreduction.dim_reduction import PCAnalysis, ICAnalysis, TSNEanalysis
from data_setter import getData
from abss.fs import currentProject

def DimReduction(cmd):
    datapath = currentProject(['datapath','src'])
    filepath = '{}\{}'.format(datapath, cmd.target)
    res, data = getData(filepath)
    if res == False:
        print('data cannot be obtaind')
        sys.exit(0)
    if cmd.method == 'ica':
        ICAnalysis(data, cmd)
    elif (cmd.method == 'pca'):
        PCAnalysis(data, cmd)
    elif (cmd.method == 'tsne'):
        TSNEanalysis(data, cmd)
    else:
        return False
    return True
