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
from abss.fs import current_project, taken
from regression.plotmaker import Plot

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

class Regressor:
    def __init__(self, cmd):
        self.cmd = cmd
        self.REPORT = None
        self.n      = None
        self.reg    = cmd.method
        if cmd.method == 'svr':
            self.REPORT['model'] = 'svr',
            self.n = taken('models', 'svr')
            self.SupportVector()
        elif (cmd.method == 'knn'):
            self.REPORT['model'] = 'knn_r',
            self.n = taken('models', 'knn_r')
            self.KNNeighbors()
        elif (cmd.method == 'dt'):
            self.REPORT['model'] = 'dtree_r',
            self.n = taken('models', 'dtree_r')
            self.DTree()
        elif (cmd.method == 'rr'):
            self.REPORT['model'] = 'ridge_r',
            self.n = taken('models', 'ridge_r')
            self.Ridge()
        elif (cmd.method == 'lr'):
            self.REPORT['model'] = 'lin_r',
            self.n = taken('models', 'lin_r')
            self.Linear()
        else:
            print('unrecognized regression code')
            return False
        self.REPORT['n'] = self.n

        self.X_train    = None
        self.X_test     = None
        self.y_train    = None
        self.y_test     = None

        self.model      = None
        self.preds      = None
        self.mse        = None

        self.state      = None
        self.SETTING    = None

    def build(self):
        datapath = current_project(['datapath','src'])
        res, self.data = get_data(datapath)
        self.y = data.pop(cmd.ref)
        self.X = CleanData(data)
        self.state, self.SETTING = setting(self.reg)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, 
                                                                self.y, 
                                                                test_size=self.SETTING['ts'], 
                                                                random_state=self.SETTING['ranst'])
        self.preds = self.model.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, self.preds)
        self.REPORT['mse'] = mse

    def SupportVector(self):
        self.model = SVR(kernel=self.SETTING['kernel'], 
                         C=self.SETTING['C'], 
                         gamma=self.SETTING['gamma'], 
                         epsilon=self.SETTING['epsilon'])
        self.model.fit(self.X_train, self.y_train)

        files = {
            'vectors': 'svr_vector_{}.png'.format(self.n),
        }
        PLOT = Plot(self.X_train, self.y_train, files['vectors'], self.model)
        PLOT.svr()
        self.REPORT['outputs'] = files

    def KNNeighbors(self):
        self.model = KNeighborsRegressor(
                n_neighbors=self.SETTING['nn'], 
                weights=self.SETTING['weights'])
        self.model.fit(self.X_train, self.y_train)

        files = {
            'knnr':'knnr_{}'.format(n),
        }
        PLOT = Plot(self.X_train, self.y_train, files['knnr'], self.model)
        PLOT.knnr()
        self.REPORT['outputs'] = files

    def DTree(self):
        self.model = DTree(max_depth=self.SETTING['depth'])
        self.model.fit(self.X, self.y)

        files = {
            'dtree':'dtree_plot_{}'.format(self.n)
        }
        PLOT = Plot(self.X_train, self.y_train, files['dtree'], self.model)
        PLOT.dtree()
        self.REPORT['outputs'] = files

    def Ridge(self):
        self.model = Ridge(alpha=self.SETTING['alpha'])
        self.model.fit(self.X_train, self.y_train)

        files = {
            'basic':'basic_ridge_{}'.format(self.n)
        }
        PLOT = Plot(self.X_train, self.y_train, files['basic'], self.model)
        PLOT.ridge()
        #s_pred = json.dumps(self.preds, cls=NumpyArrayEncoder)
        #s_coef = json.dumps(self.model.coef_, cls=NumpyArrayEncoder)
        #s_intr = json.dumps(self.model.intercept_, cls=NumpyArrayEncoder)

        #self.REPORT['preds'] = s_pred
        #self.REPORT['coeff'] = s_coef
        #self.REPORT['intercept'] = s_intr
        self.REPORT['outputs'] = files

    def Linear(cmd):
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)

        files = {
            'basic':'basic_linear_{}'.format(self.n)
        }
        PLOT = Plot(X_train, y_train, files['basic'], self.model)
        PLOT.linear()

        #s_coef = json.dumps(self.model.coef_, cls=NumpyArrayEncoder)
        #s_intr = json.dumps(self.model.intercept_, cls=NumpyArrayEncoder)

        #self.REPORT['coeffs'] = s_coef
        #self.REPORT['interc'] = s_intr
        self.REPORT['outputs'] = files
