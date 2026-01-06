
import json
import os
from abss.fs import current_project

def add(what, report):
    storypath = current_project(['storypath'])
    current = {}
    with open(storypath, 'r') as file:
        current = json.load(file)
        current[what].append(report)

    with open(storypath, 'w') as file:
        json.dump(current, file, indent=4)

def order(target, cmd):
    storypath = current_project(['storypath'])
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
    elif code == 'bp':
        return True, 'boxplots'
    elif code == 'cat':
        return True, 'categos'
    elif code == 'cdt':
        return True, 'classification_decision_tree'
    elif code == 'cm':
        return True, 'corr_matrix'
    elif code == 'dis':
        return True, 'dispersions'
    elif code == 'his':
        return True, 'histos'
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
    elif code == 'lag':
        return True, 'lagrange'
    elif code == 'che':
        return True, 'chebyshev'
    elif code == 'tay':
        return True, 'taylor'
    else:
        print('not recognized code')
        return False, None

def del_file(outputs):
    name = current_project(['project_name'])
    for k, val in outputs.items():
        filepath = 'prs\{}\outputs\{}'.format(name, val)
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print('{} does not exists'.format(filepath))

class StoryCleaner:
    def __init__(self, cmd):
        self.survivals = []
        self.indata = None
        self.code   = None
        self.data   = {}
        self.storypath = current_project(['storypath'])
        if cmd.all == False:
            res, code = set_condition(cmd.cond)
            if res == True:
                self.code = code
        self.all    = cmd.all
        self.unique = cmd.unique

        with open(self.storypath, 'r') as f:
            self.data = json.load(f)

        if(cmd.target == 'meths'):
            self.indata = 'methods'
            self.ineach = 'method'
        elif(cmd.target == 'mods'):
            self.indata = 'models'
            self.ineach = 'model'
        elif(cmd.target == 'pols'):
            self.indata = 'polys'
            self.ineach = 'poly'
        elif(cmd.target == 'exps'):
            self.indata = 'exploratory_analysis'
            self.ineach = 'metric'

    def run(self):
        if self.all == False:
            if cmd.unique == True:
                for each in self.data[self.indata]:
                    if (each[ineach] == code):
                        n = int(cmd.number)
                        if (each['n'] != n):
                            self.survivals.append(each)
                        else:
                            del_file(each['outputs'])
                    else:
                        self.survivals.append(each)
            else:
                for each in self.data[self.indata]:
                    if (each[self.ineach] != code):
                        self.survivals.append(each)
                    else:
                        del_file(each['outputs'])

        else:
            for each in self.data[self.indata]:
                del_file(each['outputs'])
        self.data[self.indata] = self.survivals
        with open(self.storypath, 'w') as f:
            json.dump(self.data, f, indent=4)
        self.message = '----story cleaned'
