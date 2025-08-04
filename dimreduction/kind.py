

from dimreduction.dim_reduction import PCAnalysis, ICAnalysis, TSNEanalysis
from data_setter import getData

def DimReduction(command):
    filepath = '{}/{}'.format(command.datapath, command.target)
    data = getData(filepath)
    if model == 'ICAnalysis':
        ICAnalysis(data, command.ref)
    elif (model == 'PCAnalysis'):
        PCAnalysis(data, command.ref)
    elif (model == 'TSNEanalysis'):
        TSNEanalysis(data, command.ref)
    else:
        return False
    return True
