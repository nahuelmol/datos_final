
from approximation.polys import Lagrange, Chebyshev, Taylor
from abss.fs import current_project

def Approximation(cmd):
    if cmd.method == 'l':
        Lagrange(cmd)
    elif (cmd.method == 'c'):
        Chebyshev(cmd)
    elif (cmd.method == 't'):
        Taylor(cmd)
    else:
       return False
    return True


