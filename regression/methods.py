from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge, LinearRegression

import numpy as np
import json

from abss.setter import setting
from abss.story import add
from abss.data_setter import get_data
from abss.fs import current_project, take_n
from regression.plotmaker import vectors_plot, ridge_r_plot, dtree_plot, knnr_plot, linear_plot

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def CleanData(data):
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    X = data.loc[:, ~data.columns.isin(cols_to_drop)]
    return X

def SupportVectorRegression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, kernel, tsize, ranst, gamma, epsilon, C = setting('SVR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=tsize, random_state=ranst)

    svr_rbf = SVR(kernel=kernel, C=C, gamma=gamma, epsilon=epsilon)
    svr_rbf.fit(X_train, y_train)
    y_pred = svr_rbf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    n = take_n('models', 'svr')
    files = {
        'vectors': 'svr_vector_{}.png'.format(n),
    }
    vectors_plot(X_train, y_train, files['vectors'], svr_rbf)
    REPORT = {
        'model':'svr',
        'mse':mse,
    }
    add('models', REPORT)

def KNearestNeighbors(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, nn, weights, ts, ranst = setting('KNNR')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=ranst)

    model = KNeighborsRegressor(n_neighbors=nn, weights=weights)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    n = take_n('models', 'knn_r')
    files = {
        'knnr':'knnr_{}'.format(n),
    }
    knnr_plot(X_train, y_train, files['knnr'], model)
    REPORT = {
        'model':'knn_r',
        'preds':pred,
    }
    add('models', REPORT)

def DecisionTree(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, depth = setting('DTree')
    model = DecisionTreeRegressor(max_depth=depth)
    model.fit(X, y)
    pred = model.predict(X_test)

    n = take_n('models', 'dtree_r')
    files = {
        'dtree':'dtree_plot_{}'.format(n)
    }
    dtree_plot(X_train, y_train, files['dtree'], model)
    REPORT = {
        'model':'dtree_r',
        'preds':pred,
    }
    add('models', REPORT)

def RidgeRegression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, alpha, ts, ranst = setting('RR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=ranst)
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    n = take_n('models', 'ridge_r')
    files = {
        'basic':'basic_ridge_{}'.format(n)
    }
    ridge_r_plot(pred, X_train, y_train, files['basic'], model)
    s_pred = json.dumps(pred, cls=NumpyArrayEncoder)
    s_coef = json.dumps(model.coef_, cls=NumpyArrayEncoder)
    s_intr = json.dumps(model.intercept_, cls=NumpyArrayEncoder)

    REPORT = {
        'model':'ridge_r',
        'preds':s_pred,
        'coeff':s_coef,
        'intercept':s_intr,
    }
    add('models', REPORT)

def LinearRegression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, ts, ranst = setting('LR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    n = take_n('models', 'lin_r')
    files = {
        'basic':'basic_linear_{}'.format(n)
    }
    linear_plot(X_train, y_train, files['basic'], model)
    REPORT = {
        'model':'lin_r',
        'coeffs':model.coef_,
        'interc':model.intercept_,
    }

    add('models', REPORT)
