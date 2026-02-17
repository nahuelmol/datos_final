
def setting(which):
    res = input('standard setting? (y/n)')
    response = {}
    if (res == 'y'):
        if (which == 'KNN'):
            return True, 5, 'auto', 'mikowski'
        elif (which == 'RNDF'):
            return True, 100, 42
        elif (which == 'dtree'):
            return True, 'POS', 'C', 'G', 1
        elif (which == 'SVC'):
            return True, 0.3, 42, 'rbf', 1, 'scale'
        elif (which == 'LOG'):
            return True, 1000
        elif (which == 'svr'):
            response['kernel']  = 'rbf' 
            response['ts']      = 0.2
            response['ranst']   = 42
            response['gamma']   = 0.1
            response['epsilon'] = 0.1
            response['C']       = 10
            return True, response
        elif (which == 'knn_r'):
            response['nn']      = 3
            response['weights'] = 'distance', 
            response['ts' ]     = 0.2
            response['ranst']   = 42
            return True, response
        elif (which == 'dt'):
            response['depth'] = 2
            return True, response
        elif (which == 'rr'):
            response['alpha'] = 1.0
            response['ts'] = 0.2
            response['ranst'] = 42
            return True, response
        elif (which == 'lr'):
            response['ts'] = 0.2
            respnose['ranst'] = 42
            return True, response
        else:
            return False, 'not recognized model'
    elif (res == 'n'):
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
            max_depth = int(input('select max depth: ')) #1
            return True, col, first, second, max_depth
        elif (which == 'SVC'):
            ts = float(input('insert ts:'))
            rs = int(input('insert rs:'))
            kernel = input('insert kernel: ')
            C = int(input('insert C:'))
            gamma = input('insert gamma')
            return True, ts, rs, kernel, C, gamma
        elif (which == 'LOG'):
            max_iter = int(input('insert max iter: '))
            return True, max_iter
        elif (which == 'SVR'):
            tsize = float(input('insert test size:'))
            ranst = int(input('random state:'))
            gamma = float(input('gamma:'))
            epsilon = float(input('epsilon:'))
            C = int(input('insert C:'))
            kernel = input('insert kernel:')
            return True, kernel, tsize, ranst, gamma, epsilon, C
        elif (which == 'KNNR'):
            nn = int(input('insert nn:'))
            weights = float(input('insert weights:'))
            ts = int(input('insert test size'))
            ranst = float(input('inert random state'))
            return True, nn, weights, ts, ranst
        elif (which == 'DTree'):
            depth = int(input('insert max depth:'))
            return True, depth
        elif (which == 'RR'):
            alpha = float('insert alpha:')
            return True, alpha
        elif (which == 'LR'):
            ts = float(input('inesrt test size:'))
            ranst = int(input('random state:'))
            return True, ts, ranst
        else:
            return False, 'not recognized model'
    else:
        return False, 'not valid response'


