import sys

from dimreduction.dim_reduction import Reductor
from abss.data_setter import get_data
from abss.fs import current_project

def DimReduction(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath, ',')
    REDUCTOR = Reductor(data, cmd)
    REDUCTOR.build()
    if res == False:
        print('data cannot be obtained')
        sys.exit(0)
    return True
