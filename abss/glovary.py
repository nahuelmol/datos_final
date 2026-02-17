import json

def setGlovar(cmd):
    data = {}
    target = ''
    if cmd.target == 'var':
        target = 'var'
    elif cmd.target == 'hvar':
        target = 'histo_var'
    elif cmd.target == 'lab':
        target = 'label'
    else:
        target = 'unknown'
        print('unknown target')

    with open('manifest.json', 'r') as f:
        data = json.load(f)
        valu = input('insert value: ')
        data['global'][target] = valu
    with open('manifest.json', 'w') as f:
        json.dump(data, f, indent=4)

