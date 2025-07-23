import os
import pandas as pd

def getData(filename):
    filepath = 'data/{}'.format(filename)
    try:
        df = pd.read_csv(filepath)
        return True, df
    except:
        return False, None

def checkAvailableData():
    datapath = 'data'
    if os.path.exists(datapath):
        cnts = os.listdir(datapath)
        if len(cnts) > 0:
            return True, cnts
        else:
            return False, None
    else:
        os.mkdir(datapath)
        return False, None

