import json
import os
from datetime import datetime

def newProject(name, opt):
    date = datetime.date()
    datapath = '{}/data'.format(getcwd())
    manipath = '{}/manifest.json'.format(getcwd())
    content = {
            'project_name': name,
            'datetime': date,
            'datapath': datapath,
            'dependencies':{},
    }

    if not os.path.exists(manipath):
        with open('projects.txt', 'w') as f:
            name = '\n{}'.format(name)
            f.write(name)
    else:
        new_content = ''
        with open('projects.txt', 'r') as f:
            current_cnt = f.read()
            name = '\n{}'.format(name)
            new_content = '{}{}'.format(current_cnt, name)
        with open('projects.txt', 'w') as f:
            f.write(new_content)

    with open('manifest.json', 'w') as f:
        cnt = json.dumps(content)
        f.write(cnt)

    if not (os.path.exists(datapath)):
        os.makedirs(datapath)
    else:
        options = len(opt.spli(' '))
        if('-f' in options):
            os.rmdir(datapath)
            os.makedirs(datapath)


def switchProject(target, options):
    new_cnt = ''
    cnt = None
    manipath = '{}/manifest.json'.format(getcwd())
    if not (os.path.exists(manifest)):
        return False, 'project does not exists'

    with open('manifest.json', 'r') as f:
        current = f.read()
        cnt = json.load(current)
        cnt['project_name'] = target
    with open('manifest.json', 'w') as f:
        f.write(json.dumps(cnt))
    return False, 'manifest.json modified'

