
import json
import os

from abss.fs import current_project
from abss.story import set_condition
from data_setter import checkAvailableData

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
        data = {}
        with open(storypath, 'r') as f:
            data = json.load(f)
        if len(data['models']) == 0:
            return True, 'there are not methods applied'
        for meth in data['models']:
            if cmd.all == True:
                print('{} - {} - {}'.format(meth['model'], meth['time'], meth['n']))
                if cmd.ac == True:
                    printGreen(meth['ac'], 'ac')
            else:
                res, code = set_condition(cmd.cond)
                if meth['model'] == code:
                    if cmd.unique == True:
                        number = 0
                        if cmd.number.isdigit():
                            number = int(cmd.number)
                        if meth['n'] == number:
                            print('{}, {}, {}'.format(meth['model'], meth['n'], meth['time']))
                    else:
                        print('{}, {}, {}'.format(meth['model'], meth['n'], meth['time']))
                        if cmd.ac == True:
                            printGreen(meth['ac'], 'ac')

    elif cmd.target == 'meths':
        data = {}
        with open(storypath, 'r') as f:
            data = json.load(f)
        if len(data['methods']) == 0:
            return True, 'there are not methods applied'
        for meth in data['methods']:
            if cmd.all == True:
                print('{} - {} - {}'.format(meth['method'], meth['time'], meth['n']))
            else:
                res, code = set_condition(cmd.cond)
                if meth['method'] == code:
                    if cmd.unique == True:
                        number = 0
                        if cmd.number.isdigit():
                            number = int(cmd.number)
                        if meth['n'] == number:
                            print('{}, {}, {}'.format(meth['method'], meth['n'], meth['time']))
                    else:
                        print('{}, {}, {}'.format(meth['method'], meth['n'], meth['time']))
                        if cmd.ac == True:
                            printGreen(meth['ac'], 'ac')

    elif cmd.target == 'exps':
        data = {}
        with open(storypath, 'r') as f:
            data = json.load(f)
        if len(data['exploratory_analysis']) == 0:
            return True, 'there are not methods applied'
        for metric in data['exploratory_analysis']:
            if cmd.all == True:
                print('{} - {} - {}'.format(metric['metric'], metric['time'], metric['n']))
            else:
                res, code = set_condition(cmd.cond)
                if metric['metric'] == code:
                    if cmd.unique == True:
                        number = 0
                        if cmd.number.isdigit():
                            number = int(cmd.number)
                        if metric['n'] == number:
                            print('{}, {}, {}'.format(metric['metric'], metric['n'], metric['time']))
                    else:
                        print('{}, {}, {}'.format(meth['metric'], meth['n'], meth['time']))

    elif cmd.target == 'tt' or cmd.target == 'tn' or cmd.target == 'src':
        ask_mani_for_data(cmd.target)
    elif cmd.target == '-cur':
        pname = current_project(['project_name'])
        print('current project {}'.format(pname))
    elif cmd.target == '-all':
        res, cnt = checkAvailableData()
        if res == False:
            print("not available data")
            sys.exit(0)
        else:
            for file in cnt:
                print(file)
    else:
        print('not recognized target')



