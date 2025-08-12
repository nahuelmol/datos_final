
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

from data_setter import getData
from dimreduction.dim_reduction import data_separator, add 
from abss.dataSetting import extract_data
from abss.fs import currentProject

def DecisionTree(cmd):
    col     = input('select column: ') #POS
    first   = input('select first possible response: ') #C
    second  = input('select second possible response: ')#G

    datapath = currentProject(['datapath','src'])
    res, data = getData(datapath)
    query   = "{}.isin(('{}', '{}'))".format(col, first, second)
    data    = data.query(query)

    data, target = data_separator(data, cmd.ref)
    TREE = DecisionTreeClassifier(max_depth=1).fit(data, target) #finds the bias
    predictions = TREE.predict(data)
    predictions[3]

    ac = accuracy_score(target, predictions)
    REPORT = {
            'method':'decisionTree',
            'time':str(datetime.now()),
            'ac':ac,
    }
    add('model', REPORT)

def Logistic(cmd):
    X_train = {}
    X_test  = {}
    y_train = {}
    y_test  = {} 
    print(cmd.test_size)
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = currentProject(['datapath','src'])
        res, data = getData(datapath)
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=cmd.test_size, random_state=cmd.random_state)
    else:
        res, result = extract_data(cmd.ref)
        X_train, X_test, y_train, y_test = result
    skyler = StandardScaler()
    X_train_scaled = skyler.fit_transform(X_train)
    X_test_scaled = skyler.transform(X_test)
    model = LogisticRegression(max_iter=1000).fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled) #making predictions over new X values (X_test)
    probs = model.predict_proba(X_test_scaled)

    #rocaucscore = roc_auc_score(y_test, probs, multi_class='ovr')
    #model2 = LogisticRegression().fit(data, target)
    #model2.predict_proba(data)

    mc = model.coef_.tolist()
    mi = model.intercept_.tolist()
    cm = confusion_matrix(y_test, predictions).tolist()
    cr = classification_report(y_test, predictions, zero_division=0)
    accuracy = accuracy_score(y_test, predictions)
    f1score = f1_score(y_test, predictions, average='macro', zero_division=0).tolist()

    REPORT = {
        'model':'logistic',
        'time':str(datetime.now()),
        'model_coef': mc,
        'model_intercept': mi,
        'confusion_matrix': cm,
        'classification_report': cr,
        'ac':accuracy,
        'f1_score':str(f1_score),
    }
    add('models', REPORT)
    

def KNearestNeighbors(cmd):
    nneigh = 5
    algorithm = 'auto'
    metric = 'minkowski'
    X_train = {}
    X_test  = {}
    y_train = {}
    y_test  = {} 
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = currentProject(['datapath','src'])
        filepath = '{}\{}'.format(datapath, cmd.target)
        res, data = getData(filepath)
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=cmd.test_size, random_state=cmd.random_state)
    else:
        X_train, X_test, y_train, y_test = extract_data(cmd.ref)

    neigh = KNeighborsClassifier(n_neighbors=nneigh)
    classifier = neigh.fit(X_train, y_train)
    
    predictions  = classifier.predict(X_test)
    proba = classifier.predict_proba(X_test)
    accuracy = accuracy_score(y_test, predictions)
    #out= classifier.neighbors()

    predictions = {
            'model':'knearest_neighbors',
            'time':str(datetime.now()),
            'ac':accuracy,
    }
    add_model('models', REPORT)


def RandomForest(data, cmd):
    X_train = {}
    X_test  = {}
    y_train = {}
    y_test  = {} 
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = currentProject(['datapath','src'])
        filepath = '{}\{}'.format(datapath, cmd.target)
        res, data = getData(filepath)
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)
    else:
        X_train, X_test, y_train, y_test = extract_data(cmd.ref)

    nestm = int(input('insert n estimators')) #100
    ranst = int(input('insert random state')) #42
    rf_classifier = RandomForestClassifier(n_estimators=nestm, random_state=ranst)
    rf_classifier.fit(X_train, y_train)

    predictions = rf_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    REPORT = {
        'model':'random_forest',
        'time':str(datetime.now()),
        'ac':accuracy,
    }
    add('models', REPORT)

def SupportVectorClassifier(cmd):
    data, target = data_separator(data, cmd.ref)
    ts = 0.3
    rs = 42
    X_train = {}
    X_test  = {}
    y_train = {}
    y_test  = {} 
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = currentProject(['datapath','src'])
        filepath = '{}\{}'.format(datapath, cmd.target)
        res, data = getData(filepath)
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=ts, random_state=rs)
    else:
        X_train, X_test, y_train, y_test = extract_data(cmd.ref)

    svc = SVC(kernel='rbf', C=1, gamma='scale')
    svc.fit(X_train, y_train)

    predictions = svc.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    REPORT = {
        'model':'support_vector_classifier',
        'time':str(datetime.now()),
        'ac':accuracy,
    }
    add('models', REPORT)
