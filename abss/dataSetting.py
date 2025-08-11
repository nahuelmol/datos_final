import json
import pandas as pd
import numpy as np

def extract_data():
    data    = []
    cnt     = {}
    X_train = np.array([])
    X_test  = np.array([])
    y_train = np.array([])
    y_test  = np.array([])
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
    for each in cnt['datapath']['test']: 
        out = pd.read_csv(each)
        if each == 'y':
            y_test = np.array(out)
        if each == 'x':
            X_test = np.array(out)

    for each in cnt['datapath']['train']:
        out = pd.reac_csv(each)
        if each == 'y':
            y_train = np.array(out)
        if each == 'x':
            X_train = np.array(out)

def delData(cmd):
    which = ''
    if cmd.target == 'tt':
        which = ['test']
    elif cmd.target == 'td':
        which = ['train']
    elif cmd.target == 'all':
        which = ['test', 'train', 'source']
    else:
        return False, 'not recognized target'
    cnt = {}
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
    
    for each in which:
        for cada in cnt['datapath'][each]:
            cnt['datapath'][each][cada] = [] 
    with open('manifest.json', 'w') as f:
        json.dump(cnt, f, indent=4)


def setData(cmd):
    cnt = {}
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
    if cmd.target == 'tt':
        print('gimme test data file')
        xpath = input('x: ')
        ypath = input('y: ')
        xpath = 'data\{}'.format(xpath)
        ypath = 'data\{}'.format(ypath)
        cnt['datapath']['test']['x'].append(xpath)
        cnt['datapath']['test']['y'].append(ypath)
    elif cmd.target == 'tn':
        print('gimme a train data file')
        xpath = input('x: ')
        ypath = input('y: ')
        xpath = 'data\{}'.format(xpath)
        ypath = 'data\{}'.format(ypath)
        cnt['datapath']['train']['x'].append(xpath)
        cnt['datapath']['train']['y'].append(ypath)
    elif cmd.target == 'src':
        file = input('gimme a source data file')
        path = 'data\{}'.format(file)
        cnt['datapath']['src'] = path
    else:
        print('not valid target')
    with open('manifest.json', 'w') as f:
        json.dump(cnt, f, indent=4)

