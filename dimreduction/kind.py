

from dimreduction.dim_reduction import PCAnalysis, ICAnalysis, TSNEanalysis
from data_setter import getData
from abss.fs import currentProject

def DimReduction(cmd):
    datapath = currentProject('datapath')
    filepath = '{}\{}'.format(datapath, cmd.target)
    res, data = getData(filepath)
    if res == False:
        print('data cannot be obtaind')
        sys.exit(0)
    if cmd.method == 'ICAnalysis':
        ICAnalysis(data, cmd)
    elif (cmd.method == 'PCAnalysis'):
        PCAnalysis(data, cmd)
    elif (cmd.method == 'TSNEanalysis'):
        TSNEanalysis(data, cmd)
    else:
        return False
    return True
