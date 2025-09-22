import sys

from .methods import LinearRegression, SupportVectorRegression, KNearestNeighbors, RidgeRegression, LinearRegression
from abss.data_setter import get_data

def Regression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    if res == False:
        print('regression failed')
        sys.exit(0)
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
