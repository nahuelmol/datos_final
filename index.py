import sys
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from methods.applyPCA import PCAnalysis
from methods.applyICA import ICAnalysis


if __name__ == "__main__":
    res, data = get_data()
    if res == False:
        print("data was not obtained")
        sys.exit(0)

    message = """
        Available Analysis
        1.PCA
        2.ICA

        Exit (press any) 
    """

    print(message)
    opc = int(input('What analysis to do?'))
    if(opc == 1):
        PCAnalysis(data)
    elif (opc == 2):
        ICAnalysis(data)
    else:
        sys.exit(0)


