
import json
import os

from abss.fs import currentProject
from data_setter import checkAvailableData, getData

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
    elif cmd.target == '-meths':
        projectname = currentProject('project_name')
        storypath = 'prs\{}\story.json'.format(projectname)
        if len(command.options) == 1:
            with open(storypath, 'r') as f:
                data = json.load(f)
                for meth in data['methods']:
                    print(meth['method'])
                    print(meth['time'])
        elif len(command.options) > 1:
            idx = command.options.index('-meths') + 1
            opc = command.options[idx]
            if opc == 'w':
                idx = command.options.index('w') + 1
                target = command.options[idx]
                with open(storypath, 'r') as f:
                    data = json.load(f)
                    for meth in data['methods']:
                        if meth['method'] == target:
                            print(meth['time'])
            else:
                print('incorrect commander {} called'.format(opc))
                print('only w commander is capable here'.format(opc))

    elif cmd.target == 'tt' or cmd.target == 'tn' or cmd.target == 'src':
        ask_mani_for_data(cmd.target)
    elif cmd.target == '-cur':
        pname = currentProject('project_name')
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



