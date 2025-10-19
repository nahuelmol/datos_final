
import pandas as pd
import json

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

from abss.data_setter import get_data
from dimreduction.dim_reduction import data_separator
from abss.story import add
from abss.dataSetting import extract_data
from abss.fs import current_project, take_n
from dimreduction.plotmaker import logistic_regression_plot, confusion_matrix_plot

def setting(which):
    res = input('do you want standard setting? (y/n)')
    if (res == 'y'):
        if (which == 'KNN'):
            return True, 5, 'auto', 'mikowski'
        elif (which == 'RNDF'):
            return True, 100, 42
        elif (which == 'DTREE'):
            return True, 'POS', 'C', 'G'
        elif (which == 'SVC'):
            return True, 0.3, 42
        else:
            return False, 'not recognized model'
    elif (res == 'n')
        if (which == 'KNN'):
            n = int(input('insert nneigh:'))
            a = input('insert algorithm:')
            m = input('insert metric:')
            return True, n, a, m
        elif (which == 'RNDF'):
            nestm = int(input('insert n estimators: '))
            ranst = int(input('insert random state:'))
            return True, nestm, ranst
        elif (which == 'DTREE'):
            col     = input('select column: ') #POS
            first   = input('select first possible response: ') #C
            second  = input('select second possible response: ')#G
            return True, col, first, second
        elif (which == 'SVC'):
            ts = float(input('insert ts:'))
            rs = int(input('insert rs:'))
            return True, ts, rs
        else:
            return False, 'not recognized model'
    else:
        return False, 'not valid response'


def split_asker():
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath)
        data, target = data_separator(data, cmd.ref)
        return X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=cmd.test_size, random_state=cmd.random_state)
    else:
        res, result = extract_data(cmd.ref)
        return X_train, X_test, y_train, y_test = result


def DecisionTree(cmd):
    res, col, first, second = setting('DTREE')
    if res == False:
        print('setting problem')

    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
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
    X_train, X_test, y_train, y_test = split_asker()

    skyler = StandardScaler()
    X_train_scaled = skyler.fit_transform(X_train)
    X_test_scaled = skyler.transform(X_test)
    model = LogisticRegression(max_iter=1000).fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled) #making predictions over new X values (X_test)
    
    #rocaucscore = roc_auc_score(y_test, probs, multi_class='ovr')
    #model2 = LogisticRegression().fit(data, target)
    #model2.predict_proba(data)

    mc = model.coef_.tolist()
    mi = model.intercept_.tolist()
    cm = confusion_matrix(y_test, predictions)
    cr = classification_report(y_test, predictions, zero_division=0)
    accuracy = accuracy_score(y_test, predictions)
    f1score = f1_score(y_test, predictions, average='macro', zero_division=0).tolist()

    n = take_n('models', 'logistic')
    files = {
        'boundary_curve': 'log_{}_boundary_curve.png'.format(n),
        'confusion_matrix': 'log_{}_confusion_matrix.png'.format(n),
    }
    logistic_regression_plot(X_train, y_train, X_test, y_test, model, files['boundary_curve'], cmd.class_)
    confusion_matrix_plot(cm, model.classes_, files['confusion_matrix'])
    REPORT = {
        'model':'logistic',
        'n':n,
        'time':str(datetime.now()),
        #'model_coef': mc,
        #'model_intercept': mi,
        #'confusion_matrix': cm.tolist(),
        'classification_report': cr,
        'ac':accuracy,
        #'f1_score':str(f1_score),
        'outputs': files,
    }
    add('models', REPORT)
    

def KNearestNeighbors(cmd):
    X_train, X_test, y_train, y_test = split_asker()
    res, nneigh, algorithm, metric = setting('KNN')
    if res == False:
        print('setting problem')

    n_models = take_models_n()
    plot_files = {
        'boundary_curve': 'log_{}_boundary_curve.png'.format(n_models),
        'confusion_matrix': 'log_{}_confusion_matrix.png'.format(n_models),
    }
    neigh = KNeighborsClassifier(n_neighbors=nneigh, algorithm=algorithm, metric=metric)
    classifier = neigh.fit(X_train, y_train)
    
    predictions  = classifier.predict(X_test)
    proba = classifier.predict_proba(X_test)
    accuracy = accuracy_score(y_test, predictions)
    #out= classifier.neighbors()

    n = take_n('models', 'knearest_neighbors')
    REPORT = {
        'model':'knearest_neighbors',
        'n':n,
        'time':str(datetime.now()),
        'ac':accuracy,
        'outputs': [],
    }
    add_model('models', REPORT)


def RandomForest(data, cmd):

    X_train, X_test, y_train, y_test = split_asker()
    res, nestm, ranst = setting('RndF')
    if res == False:
        print('setting problem')

    rf_classifier = RandomForestClassifier(n_estimators=nestm, random_state=ranst)
    rf_classifier.fit(X_train, y_train)

    predictions = rf_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    n = take_n('models', 'rand_forest')
    REPORT = {
        'model':'rand_forest',
        'n': n,
        'time':str(datetime.now()),
        'ac':accuracy,
        'outputs': [],
    }
    add('models', REPORT)

def SupportVectorClassifier(cmd):
    data, target = data_separator(data, cmd.ref)
    X_train, X_test, y_train, y_test = split_asker()
    res, ts, rs = setting('SVC')
    if res == False:
        print('setting problem')

    svc = SVC(kernel='rbf', C=1, gamma='scale')
    svc.fit(X_train, y_train)

    predictions = svc.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    n = take_n('models', 'svc')
    REPORT = {
        'model':'support_vector_classifier',
        'n': n,
        'time':str(datetime.now()),
        'ac':accuracy,
        'outputs': [],
    }
    add('models', REPORT)
