from abss.fs import currentProject

def Change(cmd):
    if cmd.changeField == '':
        return False, 'changeField must be specified'
    old = currentProject(cmd.changeField)
    content = ''
    with open('manifest.json', 'r') as file:
        content = file.read()
        content = content.replace(old, cmd.target)
    with open('manifest.json', 'w') as file:
        file.write(content)
    return True, 'change applied succesfully'


