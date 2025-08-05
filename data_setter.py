import os
import json
import pandas as pd

def getData(filepath):
    try:
        df = pd.read_csv(filepath)
        return True, df
    except:
        return False, None

def checkAvailableData():
    datapath = ''
    with open('manifest.json', 'r') as f:
        data = json.load(f)
        datapath = data['datapath']
    if os.path.exists(datapath):
        cnts = os.listdir(datapath)
        if len(cnts) > 0:
            return True, cnts
        else:
            return False, None
    else:
        os.mkdir(datapath)
        return False, None

