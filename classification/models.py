
import pandas as pd

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from datetime import datetime

from dimreduction.dim_reduction import data_separator, add_method

def DecisionTree(data, cmd):
    col     = input('select column: ') #POS
    first   = input('select first possible response: ') #C
    second  = input('select second possible response: ')#G
    query   = "{}.isin(('{}', '{}'))".format(col, first, second)
    data    = data.query(query)

    data, target = data_separator(data, cmd.ref)
    TREE = DecisionTreeClassifier(max_depth=1).fit(data, target) #finds the bias
    predictions = TREE.predict(data)
    predictions[3]

    ass = accuracy_score(target, TREE.predict(data))
    REPORT = {
            'method':'decisionTree',
            'time':str(datetime.now()),
            'ass':ass,
    }
    add_method(REPORT)

def Logistic(data, cmd):

    data, target = data_separator(data, cmd.ref)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=cmd.test_size, random_state=cmd.random_state)

    skyler = StandardScaler()
    X_train_scaled = skyler.fit_transform(X_train)
    X_test_scaled = skyler.transform(X_test)
    model = LogisticRegression(max_iter=1000).fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled) #making predictions over new X values (X_test)
    probs = model.predict_proba(X_test_scaled)

    #rocaucscore = roc_auc_score(y_test, probs, multi_class='ovr')
    #model2 = LogisticRegression().fit(data, target)
    #model2.predict_proba(data)

    cr = classification_report(y_test, predictions, zero_division=0) 
    #taking y_test values with those predicted by the model
    cm = confusion_matrix(y_test, predictions).tolist()
    accuracy = accuracy_score(y_test, predictions)
    f1score = f1_score(y_test, predictions, average='macro', zero_division=0).tolist()
    mc = model.coef_.tolist()
    mi = model.intercept_.tolist()

    """
    REPORT = {
        'method':'logistic',
        'time':str(datetime.now()),
        'model_coef': mc,
        'model_intercept': mi,
        'confusion_matrix': cm,
        'classification_report': cr,
        'as':accuracy,
        'f1_score':f1_score,
    }
    add_method(REPORT)
    """
    

def KNearestNeighbors(data, cmd):
    nneigh = 5
    algorithm = 'auto'
    metric = 'minkowski'
    y = [0,0,1,1]
    neigh = KNeighborsClassifier(n_neighbors=nneigh)
    data, target = data_separator(data, cmd.ref)
    classifier = neigh.fit(data, cmd.ref)
    
    INPUT = int(input('predict?'))
    p  = classifier.predict([INPUT])
    pp = classifier.predct_proba([INPUT])
    out= classifier.neighbors([[1.,1.,1.]])

    predictions = {
            'method':'knearest_neighbors',
            'time':str(datetime.now()),
            'p':p,
            'pp':pp,
    }
    REPORT = {
            'predictions':predictions,
    }
    add_method(REPORT)


def RandomForest(data,ref):
    y = data.pop(ref)
    X_train, X_test, y_train, y_test = train_test_split(data, y, random_state=42)

    nestm = int(input('insert n estimators')) #100
    ranst = int(input('insert random state')) #42
    rf_classifier = RandomForestClassifier(n_estimators=nestm, random_state=ranst)
    rf_classifier.fit(X_train, y_train)

    y_pred = rf_classifier.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    REPORT = {
        'method':'random_forest',
        'time':str(datetime.now()),
        'ac':accuracy,
    }
    add_method(REPORT)

def SupportVectorClassifier(data, cmd):
    data, target = data_separator(data, cmd.ref)
    test_size = 0.3
    rand_stte = 42
    X_train, X_test, y_train, y_test = train_test_split(data, target, 
                                                        test_size=test_size, random_state=rand_stte)

    model = SVC(kernel='rbf', C=1, gamma='scale')
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    REPORT = {
        'method':'support_vector_classifier',
        'time':str(datetime.now()),
        'ac':accuracy,
    }
    add_method(REPORT)
