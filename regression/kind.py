import sys

from .methods import LinearRegression, SupportVectorRegression, KNearestNeighbors, RidgeRegression, LinearRegression
from abss.data_setter import get_data
from abss.fs import current_project

def Regression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    if res == False:
        print('regression failed')
        sys.exit(0)
        return False
    if cmd.method == 'svr':
        SupportVectorRegression(data, ref)
    elif (cmd.method == 'knn'):
        KNearestNeighbors(data, ref)
    elif (cmd.method == 'dt'):
        DecisionTree(data, ref)
    elif (cmd.method == 'rr'):
        RidgeRegression(data, ref)
    elif (cmd.method == 'lr'):
        LinearRegression(data, ref)
    else:
        return False
    return True
