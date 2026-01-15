
from approximation.polys import Polymaker
from abss.fs import current_project
from abss.story import add

def Approximation(cmd):
    POLY = Polymaker(cmd)
    #POLY.set_profile()
    #POLY.reset()
    POLY.heatmap()
    #res = POLY.build_poly()
    #POLY.basic_plot()
    #POLY.polys_plot()
    #POLY.complete_plot_ipop()
    #POLY.complete_plot_ap('R')
    #POLY.create_locs()
    #POLY.add_locs()
    #POLY.boxplots('all')
    #POLY.build_grid()

    return True

