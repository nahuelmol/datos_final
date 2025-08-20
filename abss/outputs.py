import os
from abss.fs import current_project

def delOutputs(cmd):
    pname   = current_project(['project_name'])
    path    = 'prs\{}\outputs'.format(pname)
    storypath = 'prs\{}\story.json'.format(pname)
    if cmd.target == 'all':
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            print('not projects')
    elif cmd.target == 'img':
        print('delete images')
    elif cmd.target == 'spd':
        print('delete spreadsheets')
    else:
        print('not recognized target')

    data = {}
    with open(storypath, 'r') as f:
        data = json.load(f)
    data['methods']['outputs']  = []
    data['models']['outputs']   = []
    with open(stprypath, 'w') as f:
        json.dump(data, f, indent=4)
