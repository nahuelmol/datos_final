
from .models import DecisionTree, Logistic

def Classification(model, data, ref):
    if model == 'DecisionTree':
        DecisionTree(data, ref)
    elif (model == 'Logistic'):
        Logistic(data, ref)
    else:
        return False
    return True


