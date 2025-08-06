
import pandas as pd

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

def DecisionTree(data, ref):
    #ref=C
    col     = input('select column: ') #POS
    first   = input('select first possible response: ') #C
    second  = input('select second possible response: ')#G
    query = "{}.isin(('{}', '{}'))".format(col, first, second)
    data = data.query(query)

    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != ref:
                cols_to_drop.append(col)
    X = data.loc[:, ~data.columns.isin(cols_to_drop)]
    y = (data[col] == ref) # =0 if C, =1 if G 

    TREE = DecisionTreeClassifier(max_depth=1).fit(X, y) #finds the bias
    plot_tree(TREE)
    predictions = TREE.predict(X)
    predictions[3]

    AS = accuracy_score(y, TREE.predict(X))
    REPORT = {
            'as':AS
    }
    print('accuracy score: ', REPORT['as'])

def Logistic(data, ref):

    y = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    X = data.loc[:, ~data.columns.isin(cols_to_drop)]

    random_state    = int(input('Set random state: ')) #42
    test_size       = float(input('Set test size: ')) #0.2
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                        test_size=test_size, 
                                        random_state=random_state)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test) #making predictions over new X values (X_test)

    cr = classification_report(y_test, predictions) 
    #taking y_test values with those predicted by the model
    cm = confusion_matrix(y_test, predictions)
    AS = accuracy_score(y_test, predictions)
    mc = model.coef_
    mi = model.intercept_
    REPORT = {
        'model_coef': mc,
        'model_intercept': mi,
        'confusion_matrix': cm,
        'classification_report': cr,
        'as':AS
    }
    print(REPORT['model_intercept'])


def KNearestNeighbors(data):
    nneigh = 5
    algorithm = 'auto'
    metric = 'minkowski'
    y = [0,0,1,1]
    neigh = KNeighborsClassifier(n_neighbors=nneigh)
    classifier = neigh.fit(data, y)
    
    INPUT = int(input('predict?'))
    p  = classifier.predict([INPUT])
    pp = classifier.predct_proba([INPUT])
    out= classifier.neighbors([[1.,1.,1.]])

    predictions = {
            'p':p,
            'pp':pp,
    }
    REPORT = {
            'predictions':predictions,
    }


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
        'ac':accuracy,
    }

def SupportVectorClassifier(data, ref):
    y = data.pop(ref)
    X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.3, random_state=42)

    model = SVC(kernel='rbf', C=1, gamma='scale')
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    REPORT = {
        'ac':accuracy,
    }
