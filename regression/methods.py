from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge, LinearRegression

import numpy as np

from abss.setter import setting
from abss.story import add
from abss.data_setter import get_data
from abss.fs import current_project, take_n
from regression.plotmaker import vectors_plot

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
    n = take_n('models', 'logistic')
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn_regressor = KNeighborsRegressor(n_neighbors=3, weights='distance')
    knn_regressor.fit(X_train, y_train)

    new_data = np.array([[5.5]])
    prediction = knn_regressor.predict(new_data)
    REPORT = {
        'model':'knn_r',
        'preds':prediction,
    }
    add('models', REPORT)

def DecisionTree(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, depth = setting('DTree')
    regr = DecisionTreeRegressor(max_depth=depth)
    regr.fit(X, y)

    prediction = regr.predict([[2, 3]])
    REPORT = {
        'model':'dtree_r',
        'preds':prediction,
    }
    add('models', REPORT)

def RidgeRegression(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath)
    y = data.pop(cmd.ref)
    X = CleanData(data)
    res, alpha, ts, ranst = setting('RR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    ridge_model = Ridge(alpha=alpha)
    ridge_model.fit(X_train, y_train)
    predictions = ridge_model.predict(X_test)
    REPORT = {
        'model':'ridger',
        'preds':predictions,
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
    y_pred = model.predict(X_test)

    REPORT = {
        'model':'lin_r',
        'coeffs':model.coef_,
        'interc':model.intercept_,
    }

    plt.scatter(X_test, y_test, color='black', label='Actual data')
    plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Linear Regression')
    plt.xlabel('Feature')
    plt.ylabel('Target')
    plt.title('Scikit-learn Linear Regression')
    plt.legend()
    filename = 'linearRegression'
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    add('models', REPORT)
