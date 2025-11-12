import json
import os
import pandas as pd
import numpy as np

def availableFile(path):
    if os.path.exists(path):
        return True
    else:
        return False

def check_in_depth(file, sep):
    seps = ['\t', ',', ';']
    prev = 0
    with open(file, 'r') as f:
        lines = f.readlines()
        for s in seps:
            names = len(lines[0])
            for line in lines:
                if(len(line.split(s)) != names):
                    prev = seps.index(s)
                    break;
    actual = prev + 1
    return seps[actual]

def file_type(filename, tipe):
    file = filename.split('.')
    file = file[-1]
    if file == tipe:
        return True
    else:
        chech_in_depth()
        return False

def extract_data(ref):
    data    = []
    cnt     = {}
    X_train = {}
    X_test  = {}
    y_train = {}
    y_test  = {}
    if not (os.path.exists('{}\data\manifest.json'.format(os.getcwd()))):
        return False, None
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
    for each in cnt['datapath']['test']: 
        if fyle_type(each, 'tsv'):
            sep = '\t'
        elif file_type(each, 'csv'):
            sep = ','
        elif file_type(each, 'txt'):
            sep = check_in_depth(each)
        else:
            print('not type found')
        data = pd.read_csv(each, sep=sep)
        X_test, y_test = data_separator(data, ref)

    for each in cnt['datapath']['train']:
        if fyle_type(each, 'tsv'):
            sep = '\t'
        elif file_type(each, 'csv'):
            sep = ','
        elif file_type(each, 'txt'):
            sep = check_in_depth(each)
        else:
            print('not type found')
        data = pd.read_csv(each, sep=sep)
        X_train, y_train = data_separator(data, ref)

    result = X_train, X_test, y_train, y_test
    return True, result

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
        path = input(': ')
        xpath = 'data\{}'.format(path)
        cnt['datapath']['test'].append(path)
    elif cmd.target == 'tn':
        print('gimme a train data file')
        path = input(': ')
        path = 'data\{}'.format(path)
        cnt['datapath']['train'].append(path)
    elif cmd.target == 'src':
        file = input('insert filename:')
        path = '{}\data\{}'.format(os.getcwd(), file)
        res = availableFile(path)
        if res == True:
            cnt['datapath']['src'] = path
            print('----done!')
        else:
            print('----error in src')
    else:
        print('not valid target')
    with open('manifest.json', 'w') as f:
        json.dump(cnt, f, indent=4)

