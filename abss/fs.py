import json
import os
from datetime import date

def emptyManifest():
    pass

def delProject(cmd):
    manipath = '{}\manifest.json'.format(os.getcwd())
    projipath = '{}\projects.txt'.format(os.getcwd())
    if not (os.path.exists(manipath): 
        return True, 'there is not a project to delete'
    if not (os.path.exists(projipath)):
        return True, 'there is not a project to delete'

    projectname = cmd.target.strip()
    projectscnt = ''
    with open('projects.txt', 'r') as f:
        projectscnt = f.read()
    projectscnt = projectscnt.replace(projectname, "")
    with open('projects.txt', 'w') as f:
        f.write(projectscnt)
    emptyManifest(projectname)
    return True, 'project deleted'

def newProject(cmd):
    name    = cmd.target
    opt     = cmd.options
    today   = date.today().strftime("%Y-%m-%d")
    datapath = '{}\data'.format(os.getcwd())
    manipath = '{}\manifest.json'.format(os.getcwd())
    content = {
            'project_name': name,
            'datetime': today,
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

    print('datapath: ', datapath)
    if not (os.path.exists(datapath)):
        os.makedirs(datapath)
    else:
        if('-force' in opt):
            os.rmdir(datapath)
            os.makedirs(datapath)

def currentProject():
    with open('manifest.json', 'r') as f:
        current = f.read()
        cnt = json.load(current)
        return cnt['project_name']

def switchProject(target, options):
    new_cnt = ''
    cnt = None
    manipath = '{}\manifest.json'.format(os.getcwd())
    if not (os.path.exists(manifest)):
        return False, 'project does not exists'

    with open('manifest.json', 'r') as f:
        current = f.read()
        cnt = json.load(current)
        cnt['project_name'] = target
    with open('manifest.json', 'w') as f:
        f.write(json.dumps(cnt))
    return False, 'manifest.json modified'

