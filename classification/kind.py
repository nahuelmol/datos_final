
from classification.models import DecisionTree, Logistic, KNearestNeighbors, SupportVectorClassifier
from abss.fs import current_project

def Classification(cmd):
    if cmd.method == 'dt':
        DecisionTree(cmd)
    elif (cmd.method == 'l'):
        print('something')
        Logistic(cmd)
    elif (cmd.method == 'knn'):
        KNearestNeighbors(cmd)
    elif (cmd.method == 'svm'):
        SupportVectorClassifier(cmd)
    else:
        return False
    return True


