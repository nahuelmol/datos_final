
from approximation.polys import Polynomial
from abss.fs import current_project
from abss.story import add

def Approximation(cmd):
    POLY = Polynomial(cmd)
    res = POLY.build_poly()
    POLY.basic_plot()
    POLY.polys_plot()
    POLY.create_locs()
    POLY.add_locs()
    POLY.build_grid()
    add('polys', POLY.REPORT)
    return res 


