import json
import shutil
import os
from datetime import date, datetime

def outProject():
    os.remove('manifest.json')

def compare_projects():
    cleanManifest = False
    data = {}
    with open('manifest.json', 'r') as f:
        data = json.load(f)
        if data['project_name'] == cmd.target:
            cleanManifest = True
    if cleanManifest == True:
        with open('manifest.json', 'w') as f:
            data['project_name'] = ''
            data['datetime'] = ''
            data['datapath'] = ''
            data['dependencies'] = {}
            json.dump(data, f)


def delProject(cmd):
    CWD = os.getcwd()
    if cmd.target == 'all':
        if os.path.exists('prs'):
            shutil.rmtree('prs')
        if os.path.exists('manifest.json'):
            os.remove('manifest.json')
        return True, 'all projects deleted'
    projectname = cmd.target.strip()
    manipath    = '{}\manifest.json'.format(CWD)
    projipath   = '{}\prs\projects.txt'.format(CWD)
    projepath   = '{}\prs\{}'.format(CWD, projectname)
    if not (os.path.exists(manipath)):
        return True, 'there is not projects'
    if not (os.path.exists(projipath)):
        return True, 'there is not projects'

    projectscnt = ''
    with open(projipath, 'r') as f:
        projectscnt = f.read()
    projectscnt = projectscnt.replace(projectname, "")
    with open(projipath, 'w') as f:
        f.write(projectscnt)
    shutil.rmtree(projepath)
    compare_projects()
    return True, 'project deleted'

def newProject(cmd):
    name    = cmd.target.strip()
    opt     = cmd.options
    today   = date.today().strftime("%Y-%m-%d")
    datapath = '{}\data'.format(os.getcwd())
    manipath = '{}\manifest.json'.format(os.getcwd())
    data = {
        'src': datapath,
        'train':[],
        'test' :[],
    }
    content = {
            'project_name': name,
            'datetime': today,
            'datapath': data,
            'dependencies':{},
    }
    project  = 'prs'
    if not (os.path.exists(project)):
        os.mkdir(project)
        os.mkdir('prs\{}'.format(name))
        os.mkdir('prs\{}\outputs'.format(name))
        with open('prs\projects.txt', 'w') as f:
            f.write('{}'.format(name))
        with open('manifest.json', 'w') as f:
            json.dump(content, f, indent=4)
        with open('prs\{}\manifest.json'.format(name), 'w') as f:
            json.dump(content, f, indent=4)
        with open('prs\{}\story.json'.format(name), 'w') as f:
            story = {
                    'project':name,
                    'borntime':str(datetime.now()),
                    'methods':[],
                    'models':[],
            }
            json.dump(story, f, indent=4)
    else:
        new_content = ''
        with open('prs\projects.txt', 'r') as f:
            new_content = '{}\n{}'.format(f.read(), name)
        with open('prs\projects.txt', 'w') as f:
            f.write(new_content)
        os.mkdir('prs\{}'.format(name))
        os.mkdir('prs\{}\outputs'.format(name))
        with open('prs\{}\manifest.json'.format(name), 'w') as f:
            json.dump(content, f, indent=4)
        with open('prs\{}\story.json'.format(name), 'w') as f:
            story = {
                    'project':name,
                    'borntime':str(datetime.now()),
                    'methods':[],
                    'models':[],
            }
            json.dump(story, f, indent=4)


def currentProject(val):
    l = len(val)
    cnt = {}
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
    if(l == 1):
        return cnt[val[0]]
    elif(l == 2):
        return cnt[val[0]][val[1]]
    else:
        return None

def switchProject(cmd):
    projipath= 'prs\projects.txt'

    current = currentProject('project_name')
    currentpath = 'prs\{}\manifest.json'.format(current)
    targetpath  = 'prs\{}\manifest.json'.format(cmd.target)
    if (os.path.exists(targetpath) and os.path.exists(currentpath)):
        shutil.copy('manifest.json', currentpath)
        shutil.copy(targetpath, 'manifest.json')



