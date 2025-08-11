
import json
from abss.fs import currentProject

def cleanMeths(cmd):
    if cmd.all == True:
        target = ''
    else:
        target = cmd.meth
    projectname = currentProject('project_name')
    storypath = 'prs\{}\story.json'.format(projectname)
    survival_meths = []
    data = None
    with open(storypath, 'r') as f:
        data = json.load(f)
        for meth in data['methods']:
            if target == '':
                survial_meths = []
            else:
                if meth['method'] != target:
                    survival_meths.append(meth)
    data['methods'] = survival_meths
    with open(storypath, 'w') as f:
        json.dump(data, f, indent=4)

