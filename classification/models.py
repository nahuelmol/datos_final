
import pandas as pd
import numpy as np
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
from sklearn.impute import SimpleImputer
from datetime import datetime
from pandas.api.types import is_numeric_dtype

from abss.data_setter import get_data
from abss.story import add
from abss.dataSetting import extract_data
from abss.fs import current_project, taken
from abss.setter import setting

from classification.plotmaker import log_plot, cmx_plot 
from dimreduction.dim_reduction import data_separator

def check_var_type(data, ref):
    if is_numeric_dtype(data[ref]):
        new_ft = input('insert other feature: ')
        return data[new_ft]
    elif is_categorical_dtype(data[ref]):
        return data[ref]
    else:
        print('not recognized variable type:')
        new_ft = input('insert feature with recognizable type: ')
        return data[new_ft]

def check_to_impute(X):
    if (np.isnan(X).any() == False) and (np.isinf(X).any() == False):
        return X
    else:
        where = np.where(np.isnan(X))[0]
        print('NaN: {}\nidx: {}'.format(np.isnan(X).any(), where))
        print('infinite:', np.isinf(X).any())
        print("cleaning")
        imputer = SimpleImputer(strategy='mean') #median, most_frequent
        X = imputer.fit_transform(X)
        return X


def split_asker(cmd):
    res = input('split original data?')
    if(res == 's' or res == 'S' or res == 'si' or res == 'Si'):
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath, ',')
        cmd.ref = check_var_type(data, cmd.ref)
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=cmd.test_size, random_state=cmd.random_state)
        return True, X_train, X_test, y_train, y_test
    else:
        res, result = extract_data(cmd.ref)
        X_train, X_test, y_train, y_test = result
        return True, X_train, X_test, y_train, y_test

class Classifier:
    def __init__(self, cmd):
        self.cmd = cmd
        if cmd.method == 'dt':
            self.classification = 'Tree'
        elif (cmd.method == 'l'):
            self.classification = 'Logistic' 
        elif (cmd.method == 'knn'):
            self.classification = 'KNN' 
        elif (cmd.method == 'svm'):
            self.classification = 'SVC' 

        datapath = current_project(['datapath','src'])
        res, self.data = get_data(datapath, ',')

        self.classifier = None
        self.target     = None
        self.n          = None
        self.accur      = None
        self.files      = None

        self.X_train    = None
        self.X_test     = None
        self.y_train    = None
        self.y_test     = None

        self.X_train_scaled = None
        self.X_test_scaled  = None

    def build(self):
        self.X_train, self.X_test, self.y_train, self.y_test = split_asker(cmd)
        if (self.classification == 'Logistic'):
            self.REPORT['method']   = 'logistic'
            self.n = taken('models', 'logistic')
            self.Logistic(cmd)
        elif (self.classification == 'Tree'):
            self.REPORT['method']   = 'decisionTree'
            self.n = taken('models', 'decisionTree')
            self.DecisionTree(cmd)
        elif (self.classification == 'SVC'):
            self.REPORT['method']   = 'svc'
            self.n = taken('models', 'svc')
            self.SupportVector(cmd)
        elif (self.classification == 'KNN'):
            self.REPORT['method']   = 'knearest_neighbors'
            self.n = taken('models', 'knearest_neighbors')
            self.KNearestNeighbors(cmd)
        elif (self.classification == 'RandomForest'):
            self.REPORT['method']   = 'rand_forest'
            self.n = taken('models', 'rand_forest')
            self.RandomForest(cmd)
        else:
            print('not recognized classification algorithm')
        preds = classifier.predict(self.data)
        self.accur = accuracy_score(self.target, preds)
        self.REPORT['ac']       = self.accur
        self.REPORT['time']     = str(datetime.now())
        self.REPORT['outputs']  = self.files

    def DecisionTree(self):
        res, col, first, second, max_depth = setting('DTREE')
        if res == False:
            print('setting problem')

        query   = "{}.isin(('{}', '{}'))".format(col, first, second)
        data    = data.query(query)

        self.data, self.target = data_separator(data, self.cmd.ref)
        self.classifier = DecisionTreeClassifier(max_depth=max_depth)
        self.classifier.fit(self.data, self.target)
        self.files = {}

    def Logistic(self):
        X_train, X_test, y_train, y_test = split_asker(cmd)
        res, max_iter = setting('LOG')
        if res == False:
            print("setting problem")

        skyler = StandardScaler()
        self.X_train_scaled = skyler.fit_transform(X_train)
        self.data = skyler.transform(X_test) #X_test_scaled 
        X_train_imputed = check_to_impute(self.X_train_scaled)

        classifier = LogisticRegression(max_iter=max_iter)
        classifier.fit(self.X_train_scaled, y_train)
    
        mc = classifier.coef_.tolist()
        mi = classifier.intercept_.tolist()
        cm = confusion_matrix(y_test, preds)
        cr = classification_report(y_test, preds, zero_division=0)
        #f1score = f1_score(y_test, predictions, average='macro', zero_division=0).tolist()

        files = {
            'boundary_curve': 'log_{}_boundary_curve.png'.format(self.n),
            'confusion_matrix': 'log_{}_confusion_matrix.png'.format(self.n),
        }
        log_plot(self.X_train, self.y_train, self.X_test, self.y_test, classifier, files['boundary_curve'], cmd.class_)
        cmx_plot(cm, classifier.classes_, files['confusion_matrix'])
        #'model_coef': mc,
        #'model_intercept': mi,
        #'confusion_matrix': cm.tolist(),
        #'f1_score':str(f1_score),
        self.REPORT['classification_report'] = cr
        self.REPORT['outputs'] = files

    def KNearestNeighbors(cmd):
        res, nneigh, algorithm, metric = setting('KNN')
        if res == False:
            print('setting problem')

        n_models = take_models_n()
        files = {
            'boundary_curve': 'log_{}_boundary_curve.png'.format(n_models),
            'confusion_matrix': 'log_{}_confusion_matrix.png'.format(n_models),
        }
        classifier = KNeighborsClassifier(n_neighbors=nneigh, algorithm=algorithm, metric=metric)
        classifier.fit(X_train, y_train)
    
        preds = classifier.predict(X_test)
        #proba = classifier.predict_proba(X_test)
        self.accur = accuracy_score(y_test, preds)
        self.REPORT['outputs'] = files

    def RandomForest(data, cmd):
        res, nestm, ranst = setting('RndF')
        if res == False:
            print('setting problem')

        classifier = RandomForestClassifier(n_estimators=nestm, random_state=ranst)
        classifier.fit(self.X_train, self.y_train)

        self.REPORT['outputs'] = {}

    def SupportVector(cmd):
        data, target = data_separator(data, cmd.ref)
        X_train, X_test, y_train, y_test = split_asker(cmd)
        res, ts, rs, kernel, C, gamma = setting('SVC')
        if res == False:
            print('setting problem')

        classifier = SVC(kernel=kernel, C=C, gamma=gamma)
        classifier.fit(X_train, y_train)

        self.REPORT['outputs'] = {}
