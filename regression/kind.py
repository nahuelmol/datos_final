from .methods import LinearRegression, SupportVectorRegression, KNearestNeighbors, RidgeRegression, LinearRegression
from data_setter import getData

def Regression(command):
    datapath = currentProject(['datapath','src'])
    filepath = '{}\{}'.format(datapath, cmd.target)
    data = getData(filepath)
    if cmd.method == 'SVR':
        SupportVectorRegression(data, ref)
    elif (cmd.method == 'knneighbors'):
        KNearestNeighbors(data, ref)
    elif (cmd.method == 'decisiontree'):
        DecisionTree(data, ref)
    elif (cmd.method == 'ridgeregression'):
        RidgeRegression(data, ref)
    elif (cmd.method == 'linearregression'):
        LinearRegression(data, ref)
    else:
        return False
    return True
