import sys

from dimreduction.dim_reduction import PCAnalysis, ICAnalysis, TSNEanalysis
from abss.data_setter import get_data
from abss.fs import current_project

def DimReduction(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath, ',')
    if res == False:
        print('data cannot be obtained')
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
