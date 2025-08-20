
import json
import os
from abss.fs import current_project

def order(target, cmd):
    pname = current_project(['project_name'])
    storypath = 'prs\{}\story.json'.format(pname)
    data = {}
    with open(storypath, 'r') as f:
        data = json.load(f)
    with open(storypath, 'w') as f:
        for idx, item in enumerate(data[target]):
            new_n = idx + 1
            old_n = data[target][idx]['n']
            data[target][idx]['n'] = new_n
            for k, v in data[target][idx]['outputs'].items():
                old_filename = v #this is value, the filename
                new_filename = v.replace(str(old_n), str(new_n))
                data[target][idx]['outputs'][k] = new_filename
                path_old = 'prs\{}\outputs\{}'.format(pname, old_filename)
                path_new = 'prs\{}\outputs\{}'.format(pname, new_filename)
                os.rename(path_old, path_new)
        json.dump(data, f, indent=4)
    print('----ordered')

def set_condition(code):
    if code == 'log':
        return True, 'logistic' 
    elif code == 'cdt':
        return True, 'classification_decision_tree'
    elif code == 'knn':
        return True, 'classification_knearest_neigh'
    elif code == 'rf':
        return True, 'random_forest'
    elif code == 'rr':
        return True, 'ridge_regression'
    elif code == 'lin':
        return True, 'linear_regression'
    elif code == 'rdt':
        return True, 'regression_decision_tree'
    elif code == 'pca':
        return True, 'pca'
    elif code == 'ica':
        return True, 'ica'
    elif code == 'tsne':
        return True, 'tsne'
    else:
        print('not recognized code')
        return False, None

def del_file(outputs):
    name = current_project(['project_name'])
    for k, val in outputs.items():
        filepath = 'prs\{}\outputs\{}'.format(name, val)
        if os.path.exists(filepath):
            os.remove(filepath)


def story_cleaner(cmd):
    pname = current_project(['project_name'])
    storypath = 'prs\{}\story.json'.format(pname)
    data = {}
    survivals = []
    with open(storypath, 'r') as f:
        data = json.load(f)
    if cmd.target == 'meths':
        if cmd.all == False:
            res, code = set_condition(cmd.cond)
            if cmd.unique == True:
                for each in data['methods']:
                    if (each['method'] == code):
                        n = int(cmd.number)
                        if (each['n'] != n):
                            survivals.append(each)
                        else:
                            del_file(each['outputs'])
            else:
                for each in data['methods']:
                    if (each['method'] != code):
                        survivals.append(each)
                    else:
                        del_file(each['outputs'])
        data['methods'] = survivals

    elif cmd.target == 'mods':
        if cmd.all == False:
            res, code = set_condition(cmd.cond)
            if cmd.unique == True:
                    for each in data['models']:
                        n = int(each['n'])
                        if (each['model'] != code and n != cmd.number):
                            survivals.append(each)
            else:
                for each in data['models']:
                    if (each['model'] != code):
                        survivals.append(each)
        data['models'] = survivals
    else:
        return False, 'not available target'
    with open(storypath, 'w') as f:
        json.dump(data, f, indent=4)
    return True, '----story cleaned'

