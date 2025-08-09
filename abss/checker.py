
import json
import os

from abss.fs import currentProject
from data_setter import checkAvailableData, getData

def lookFor(fileType):
    datapath = ''
    files = []
    if not os.path.exists('{}/manifest.json'.format(getwd())):
        return True, 'not existent project'
    with open('manifest.json', 'r') as f:
        data = json.load(f)
        datapath = data['datapath']
    for each in datapath:
        listFile = each.split('.')
        if listFile[-1] == 'csv':
            files.append(each)
            return False, files
    if len(files) == 0:
        return False, 'there is not files with that extension'


def checker(command):
    if '-d' in command.options:
        idx = options.index('-d')
        if(options(idx + 1) == '-ft'):
            filetype = options.index(idx + 2)
            if(filetype == 'tsv'):
                err, msg = lookFor('tsv')
                if err:
                    print(msg)
                else:
                    print('content {}', msg)
            elif(filetype == 'csv'):
                err, msg = lookFor('csv')
                if err:
                    print(msg)
                else:
                    print('content {}', msg)
            else:
                print('not recognized value')
    elif '-meths' in command.options:
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
                print('incorrect commander {} calld'.format(opc))
                print('only w commander is capable here'.format(opc))

    elif '-cur' in command.options:
        print('current project')
    elif '-all' in command.options:
        res, cnt = checkAvailableData()
        if res == False:
            print("not available data")
            sys.exit(0)
        else:
            for file in cnt:
                print(file)
    else:
        print('sending check command information')



