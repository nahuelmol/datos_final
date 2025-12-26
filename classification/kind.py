
from classification.models import Classifier
from abss.story import add

def Classification(cmd):
    CLASSIFIER = Classifier(cmd)
    CLASSIFIER.build()
    add('models', CLASSIFIER.REPORT)
    return True


