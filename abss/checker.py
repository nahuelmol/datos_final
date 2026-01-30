import json
import os

from abss.fs import current_project
from abss.story import set_condition
from abss.data_setter import checkAvailableData

def printGreen(text, what):
    print(text , f"\033[32m {what} \033[0m")
    print(f"\033[32m {text}\033[0m")

def takeType(file, ft):
    if not os.path.exists('{}/manifest.json'.format(os.getcwd())):
        return True, 'not existent project'
    listFile = file.split('.')
    if listFile[-1] == ft:
        print(file)

def ask_mani_for_data(what):
    path = '{}\manifest.json'.format(os.getcwd())
    if os.path.exists(path):
        data = {}
        with open('manifest.json', 'r') as f:
            data = json.load(f)
        res = []
        if what == 'tt':
            res.append(data['datapath']['test']['x'])
            res.append(data['datapath']['test']['y'])
        elif what == 'tn':
            res.append(data['datapath']['train']['x'])
            res.append(data['datapath']['train']['y'])
        elif what == 'src':
            t = data['datapath']['src']
            if len(t) > 0:
                print(t)
            else:
                print('not source')
        else:
            print('not found target')

        if len(res[0]) == 0:
            print('not data for {}: x'.format(what))
        else:
            print('{}: x: {}'.format(what, res[0]))

        if len(res[1]) == 0:
            print('not data for {}: y'.format(what))
        else:
            print('{}: y: {}'.format(what, res[1]))
    else:
        print('manifest does not exists')

def memocheck(cmd):
    data = {}
    it = ''
    which = ''
    storypath = current_project(['storypath'])
    with open(storypath, 'r') as f:
        data = json.load(f)
    if cmd.target == 'mods':
        which = 'models'
        it = 'model'
    elif cmd.target == 'meths':
        which = 'methods'
        it = 'method'
    elif cmd.target == 'exps':
        which = 'exploratory_analysis'
        it = 'metric'
    elif cmd.target == 'pols':
        which = 'polys'
        it = 'poly'
    else:
        return False, 'wrong target'
    if len(data[which]) == 0:
        return False, 'there are not methods applied'

    for each in data[which]:
        if cmd.all == True:
            print('{} - {} - {}'.format(each[it], each['time'], each['n']))
            if cmd.ac == True:
                printGreen(each['ac'], 'ac')
            return True, '--done--'
        else:
            res, code = set_condition(cmd.cond)
            if each[it] == code:
                if cmd.unique == True:
                    number = 0
                    if cmd.number.isdigit():
                        number = int(cmd.number)
                    if each['n'] == number:
                        print('{}, {}, {}'.format(each[it], each['n'], each['time']))
                else:
                    print('{}, {}, {}'.format(each[it], each['n'], each['time']))
                    if cmd.ac == True:
                        printGreen(each['ac'], 'ac')
            return True, '--done--'

def checker(cmd):
    storypath = current_project(['storypath'])
    if cmd.target == 'file':
        ft = cmd.currentFlags['-ft']
        src= current_project(['datapath', 'src'])
        files = os.listdir(src)
        if '-ft' in cmd.currentFlags:
            for file in files:
                takeType(file, ft)
        elif '-all' in cmd.currentFlags:
            for file in files:
                print('file: ', file)
    elif cmd.target == 'mods':
        res, msg = memocheck(cmd)
        if res == False:
            print(msg)
        return True, '----done----mods'

    elif cmd.target == 'meths':
        res, msg = memocheck(cmd)
        if res == False:
            print(msg)
        return True, '----done----meths'

    elif cmd.target == 'exps':
        res, msg = memocheck(cmd)
        if res == False:
            print(msg)
        return True, '----done----exps'

    elif cmd.target == 'pols':
        res, msg = memocheck(cmd)
        if res == False:
            print(msg)
        return True, '----done----pols'

    elif cmd.target == 'tt' or cmd.target == 'tn' or cmd.target == 'src':
        ask_mani_for_data(cmd.target)
    elif cmd.target == '-cur':
        pname = current_project(['project_name'])
        print('current project {}'.format(pname))
        return True, '----done----curr----'
    elif cmd.target == '-all':
        res, cnt = checkAvailableData()
        if res == False:
            return False, 'not available data'
        for file in cnt:
            print(file)
    else:
        msg = 'not recognized target'
        return False, msg
    return True, '----done----'



