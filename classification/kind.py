
from classification.models import DecisionTree, Logistic, KNearestNeighbors, SupportVectorClassifier

def Classification(cmd):
    CLASSIFIER = Classifier(cmd)
    CLASSIFIER.build()
    add('models', CLASSIFIER.REPORT)
    """
    if cmd.method == 'dt':
        DecisionTree(cmd)
    elif (cmd.method == 'l'):
        Logistic(cmd)
    elif (cmd.method == 'knn'):
        KNearestNeighbors(cmd)
    elif (cmd.method == 'svm'):
        SupportVectorClassifier(cmd)
    else:
        return False
    return True
    """
    return True


