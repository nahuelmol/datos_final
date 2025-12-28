
from explo.exploratories import Explorer
from abss.fs import current_project
from abss.data_setter import get_data
from abss.story import add

def ExploratoryAnalysis(cmd):
    datapath = current_project(['datapath', 'src'])
    res, data = get_data(datapath, ',')
    EXPLORER = Explorer(data, cmd)
    EXPLORER.build()
    add('exploratory_analysis', EXPLORER.REPORT)
    return True, EXPLORER.MSG

