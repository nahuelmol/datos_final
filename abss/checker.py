
import json
import os

from abss.fs import currentProject
from data_setter import checkAvailableData, getData

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
    if cmd.target == 'file':
        if '-ft' in cmd.currentFlags:
            ft = cmd.currentFlags['-ft']
            src= currentProject(['datapath', 'src'])
            files = os.listdir(src)
            for file in files:
                takeType(file, ft)
        elif '-all' in cmd.currentFlags:
            ft = cmd.currentFlags['-ft']
            src= currentProject(['datapath', 'src'])
            files = os.listdir(src)
            for file in files:
                print('file: ', file)
    elif cmd.target == '-mods':
        projectname = currentProject(['project_name'])
        storypath = 'prs\{}\story.json'.format(projectname)
        if cmd.all == True:
            data = {}
            with open(storypath, 'r') as f:
                data = json.load(f)
                for meth in data['models']:
                    print(meth['model'])
                    if cmd.ac == True:
                        printGreen(meth['ac'], 'ac')
                    else:
                        print(meth['time'])

        else:
            with open(storypath, 'r') as f:
                data = json.load(f)
                for meth in data['methods']:
                    if meth['method'] == cmd.cond:
                        print(meth['time'])

    elif cmd.target == '-meths':
        projectname = currentProject(['project_name'])
        storypath = 'prs\{}\story.json'.format(projectname)
        if cmd.all == True:
            with open(storypath, 'r') as f:
                data = json.load(f)
                for meth in data['methods']:
                    print(meth['method'])
                    print(meth['time'])
        else:
            with open(storypath, 'r') as f:
                data = json.load(f)
                for meth in data['methods']:
                    if meth['method'] == cmd.cond:
                        print(meth['time'])

    elif cmd.target == 'tt' or cmd.target == 'tn' or cmd.target == 'src':
        ask_mani_for_data(cmd.target)
    elif cmd.target == '-cur':
        pname = currentProject(['project_name'])
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
        print('sending check command information')



