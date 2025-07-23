
from models import DecisionTree, Logistic

def Classification(model, data):
    if model == 'DecisionTree':
        DecisionTree(data)
    elif (model == 'Logistic'):
        Logistic(data)
    else:
        return False
    return True


