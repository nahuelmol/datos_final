
from classification.models import DecisionTree, Logistic

def Classification(command):
    filepath = '{}/{}'.format(command.datapath, command.target)
    data = getData(filepath)
    opc = command.method
    if opc == 'DecisionTree':
        DecisionTree(data, command.ref)
    elif (opc == 'Logistic'):
        Logistic(data, command.ref)
    elif (opc == 'KNearestNeighbors'):
        KNearestNeighbors(data, command.ref)
    elif (opc == 'RandomForest'):
        KNearestNeighbors(data, command.ref)
    elif (opc == 'SupportVectorMachine'):
        SupportVectorMachine(data, command.ref)
    else:
        return False
    return True


