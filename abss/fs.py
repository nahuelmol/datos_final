import json
import shutil
import os
import pandas as pd
from datetime import date, datetime

def current_project(val):
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
        for key in val:
            cnt = cnt[key]
        return cnt

def write_csv(df, name):
    pname = current_project(['project_name'])
    path = 'prs\{}\outputs'.format(pname)
    path = '{}\{}'.format(path, name)
    if not isinstance(df, pd.DataFrame):
        print('getting: {}.{}'.format(type(df).__module__, type(df).__name__))
        return False, '---not a correct dataframe served'
    if os.path.exists(path):
        res = input('file already exists, overwrite?')
        if res == 's':
            df.to_csv(name)
            return True, '----file already exists, overwritten'
        else:
            return False, '----file not written'
    else:
        df.to_csv(path)
        return True, '----written'

def return_each(plural):
    if plural == 'methods':
        return 'method'
    elif plural == 'models':
        return 'model'
    elif plural == 'exploratory_analysis':
        return 'metric'

def take_n(on, typeof):
    pname = current_project(['project_name'])
    with open('prs\{}\story.json'.format(pname), 'r') as f:
        data    = json.load(f)
        aux     = 0
        for each in data[on]:
            name = return_each(on)
            if each[name] == typeof:
                n = int(each['n'])
                if n > aux:
                    aux = n
        return (aux + 1)

def outProject():
    os.remove('manifest.json')

def compare_projects(cmd):
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
            json.dump(data, f, indent=4)


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
    compare_projects(cmd)
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
            'storypath': 'prs\{}\story.json'.format(name),
            'global': {
                'var': None,
                'label': None,
                'hvar': None,
            },
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
                    'exploratory_analysis':[],
                    'methods':[],
                    'models':[],
                    'polyis':[],
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

def switchProject(cmd):
    projipath= 'prs\projects.txt'

    current = current_project('project_name')
    currentpath = 'prs\{}\manifest.json'.format(current)
    targetpath  = 'prs\{}\manifest.json'.format(cmd.target)
    if (os.path.exists(targetpath) and os.path.exists(currentpath)):
        shutil.copy('manifest.json', currentpath)
        shutil.copy(targetpath, 'manifest.json')

