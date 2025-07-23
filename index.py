import sys
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from methods.applyPCA import PCAnalysis
from methods.applyICA import ICAnalysis

from classification.kind import Classification


if __name__ == "__main__":
    res, data = get_data()
    if res == False:
        print("data was not obtained")
        sys.exit(0)

    message = """
        Available Analysis
        1.PCA
        2.ICA
        3.Classification problem -> Decision Tree

        Exit (press any) 
    """

    print(message)
    opc = int(input('What analysis to do?'))
    if(opc == 1):
        PCAnalysis(data)
    elif (opc == 2):
        ICAnalysis(data)
    elif (opc == 3):
        working = Classification('DecisionTree', data)
        if working:
            print('working')
        else:
            print('not working')
    else:
        sys.exit(0)


