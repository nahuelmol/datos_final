
from approximation.polys import Lagrange, Chebyshev, Taylor
from abss.fs import current_project

def Approximation(cmd):
    if cmd.method == 'Lag':
        Lagrange(cmd)
    elif (cmd.method == 'Chev'):
        Chebyshev(cmd)
    elif (cmd.method == 'Taylor'):
        Taylor(cmd)
    else:
       return False
    return True


