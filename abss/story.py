
import json
from abss.fs import currentProject

def set_condition(code):
    if code == 'lr':
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

def story_cleaner(cmd):
    target  = ''
    coll    = ''
    to      = ''
    if cmd.all == False:
        if cmd.target == 'meths':
            coll = 'methods'
            to = 'method'
        elif cmd.target == 'mods':
            coll = 'models'
            to = 'model'
        res, target = set_condition(cmd.cond)
        if res == False:
            return False, None
    pname = currentProject(['project_name'])
    storypath = 'prs\{}\story.json'.format(pname)
    survivals = []
    data = None
    with open(storypath, 'r') as f:
        data = json.load(f)
        for each in data[coll]:
            if cmd.all == True:
                survivals = []
            else:
                if each[to] != target:
                    survivals.append(each)
    data[coll] = survivals
    with open(storypath, 'w') as f:
        json.dump(data, f, indent=4)

