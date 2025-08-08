import json
import shutil
import os
from datetime import date, datetime

def outProject():
    os.remove('manifest.json')

def delProject(cmd):
    manipath = '{}\manifest.json'.format(os.getcwd())
    projipath = '{}\prs\projects.txt'.format(os.getcwd())
    if not (os.path.exists(manipath)):
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
    os.remove(manipath)
    return True, 'project deleted'

def newProject(cmd):
    name    = cmd.target.strip()
    print(name)
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
    project  = 'prs'
    if not (os.path.exists(project)):
        os.mkdir(project)
        os.mkdir('prs\{}'.format(name))
        os.mkdir('prs\{}\outputs'.format(name))
        with open('prs\projects.txt', 'w') as f:
            f.write('\n{}'.format(name))
        with open('manifest.json', 'w') as f:
            json.dump(content, f, indent=4)
        with open('prs\{}\story.json'.format(name), 'w') as f:
            story = {
                    'project':name,
                    'borntime':str(datetime.now()),
                    'methods':[],
            }
            json.dump(story, f, indent=4)
    else:
        with open('prs\projects.txt', 'r') as f:
            name = '{}\n'.format(name)
            new_content = '{}{}'.format(f.read(), name)
        os.mkdir('prs\{}'.format(name))
        shutil('manifest.json', '{}\manifest.json'.format(pathproject))
        with open('manifest.json', 'r') as f:
            f.write(content)


def currentProject(value):
    with open('manifest.json', 'r') as f:
        cnt = json.load(f)
        return cnt[value]

def switchProject(target, options):
    manipath = '{}\manifest.json'.format(os.getcwd())
    projipath= 'prs\projects.txt'

    os.remove(manipath)
    if not (os.path.exists('prs\{}\manifest.json'.format(target))):
        shutil.copy('prs\{}\manifest.json'.format(target), 'manifest.json')



