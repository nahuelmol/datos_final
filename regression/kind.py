import sys

from .methods import LinRegression, SupportVectorRegression, KNearestNeighbors, RidgeRegression, LinearRegression

def Regression(cmd):
    if cmd.method == 'svr':
        SupportVectorRegression(cmd)
    elif (cmd.method == 'knn'):
        KNearestNeighbors(cmd)
    elif (cmd.method == 'dt'):
        DecisionTree(cmd)
    elif (cmd.method == 'rr'):
        RidgeRegression(cmd)
    elif (cmd.method == 'lr'):
        LinRegression(cmd)
    else:
        return False
    return True
