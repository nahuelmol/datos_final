from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge, LinearRegression

import numpy as np

from abss.setter import setting

def CleanData(data):
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            cols_to_drop.append(col)
    X = data.loc[:, ~data.columns.isin(cols_to_drop)]
    return X

def SupportVectorRegression(data, ref):
    y = data.pop(ref)
    X = CleanData(data)
    kernel, tsize, ranst, gamma, epsilon, C = setting('SVR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=tsize, random_state=ranst)

    svr_rbf = SVR(kernel='rbf', C=C, gamma=gamma, epsilon=epsilon)
    svr_rbf.fit(X_train, y_train)
    y_pred = svr_rbf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    REPORT = {
        'mse':mse,
    }

def KNearestNeighbors(data, ref):
    y = data.pop(ref)
    X = CleanData(data)
    nn, weights, ts, ranst = setting('KNNR')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn_regressor = KNeighborsRegressor(n_neighbors=3, weights='distance')
    knn_regressor.fit(X_train, y_train)

    new_data = np.array([[5.5]])
    prediction = knn_regressor.predict(new_data)
    REPORT = {
        'preds':prediction,
    }

def DecisionTree(data, ref):
    y = data.pop(ref)
    X = CleanData(data)
    depth = setting('DTree')
    regr = DecisionTreeRegressor(max_depth=depth)
    regr.fit(X, y)

    prediction = regr.predict([[2, 3]])
    REPORT = {
        'preds':prediction,
    }

def RidgeRegression(data, ref):
    y = data.pop(ref)
    X = CleanData(data)
    alpha, ts, ranst = setting('RR')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    ridge_model = Ridge(alpha=alpha)
    ridge_model.fit(X_train, y_train)
    predictions = ridge_model.predict(X_test)
    REPORT = {
            'preds':predictions,
    }

def LinearRegression(data, ref):
    y = data.pop(ref)
    X = CleanData(data)
    ts, ranst = setting('LR')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    REPORT = {
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
