
import json
from abss.fs import currentProject

def story_cleaner(to, cmd):
    if cmd.all == True:
        target = ''
    else:
        if to == 'methods':
            target = cmd.meth
        elif to == 'models':
            target = cmd.mod
        else:
            print('not recognized to')
    projectname = currentProject(['project_name'])
    storypath = 'prs\{}\story.json'.format(projectname)
    survivals = []
    data = None
    with open(storypath, 'r') as f:
        data = json.load(f)
        for each in data[to]:
            if target == '':
                survials = []
            else:
                if each[to] != target:
                    survivals.append(each)
    data[to] = survivals
    with open(storypath, 'w') as f:
        json.dump(data, f, indent=4)

