
from classification.models import DecisionTree, Logistic, KNearestNeighbors, SupportVectorClassifier

def Classification(cmd):
    filepath = '{}/{}'.format(cmd.datapath, cmd.target)
    data = getData(filepath)
    if cmd.method == 'DecisionTree':
        DecisionTree(data, cmd.ref)
    elif (cmd.method == 'Logistic'):
        Logistic(data, cmd.ref)
    elif (cmd.method == 'KNearestNeighbors'):
        KNearestNeighbors(data, cmd.ref)
    elif (cmd.method == 'RandomForest'):
        KNearestNeighbors(data, cmd.ref)
    elif (cmd.method == 'SupportVectorMachine'):
        SupportVectorClassifier(data, cmd.ref)
    else:
        return False
    return True


