
from classification.models import DecisionTree, Logistic, KNearestNeighbors, SupportVectorClassifier
from abss.fs import currentProject
from data_setter import getData

def Classification(cmd):
    datapath = currentProject(['datapath','src'])
    filepath = '{}\{}'.format(datapath, cmd.target)
    res, data = getData(filepath)
    if res == False:
        print('data cannot be obtaind')
    if cmd.method == 'dt':
        DecisionTree(data, cmd)
    elif (cmd.method == 'l'):
        Logistic(data, cmd)
    elif (cmd.method == 'knn'):
        KNearestNeighbors(data, cmd)
    elif (cmd.method == 'svm'):
        SupportVectorClassifier(data, cmd)
    else:
        return False
    return True


