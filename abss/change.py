from abss.fs import current_project

def Change(cmd):
    if cmd.changeField == '':
        return False, 'changeField must be specified'
    old = current_project(cmd.changeField)
    content = ''
    with open('manifest.json', 'r') as file:
        content = file.read()
        content = content.replace(old, cmd.target)
    with open('manifest.json', 'w') as file:
        file.write(content)
    return True, 'change applied succesfully'


