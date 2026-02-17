from abss.fs import current_project
from abss.data_setter import get_data

def list_vars(cmd):
    datapath = current_project(['datapath', 'src'])
    res, data = get_data(datapath)
    if cmd.varType == 'n':
        for col in data.select_dtypes(include=["number"]).columns:
            print(col)
    elif cmd.varType == 'c':
        for col in data.select_dtypes(include=["object", "category"]).columns:
            print('{} - {}'.format(col, data[col].nunique()))
    elif cmd.varType == 's':
        for col in data.select_dtypes(include=["object", "string"]).columns:
            print(col)
    else:
        print('unrecognized vartype')

def list_labs(cmd):
    datapath = current_project(['datapath', 'src'])
    res, data = get_data(datapath)
    for label in data.index:
        print(label)

