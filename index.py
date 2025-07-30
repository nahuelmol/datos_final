import sys
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from methods.dim_reduction import PCAnalysis, ICAnalysis, TSNEanalysis

from classification.kind import Classification
from data_setter import checkAvailableData, getData

if __name__ == "__main__":
    message = """

        Available Datasets

    """
    print(message)
    res, dataAv = checkAvailableData()
    if res:
        i=1
        for data in dataAv:
            print('{}.{}'.format(i, data))
            i+=1
    else:
        print('not data available')
        sys.exit(0)
    print("\n\n")
    opc = int(input("select one option: "))
    filename = dataAv[opc-1]
    res, data = getData(filename)
    if res == False:
        print("data was not obtained")
        sys.exit(0)

    message = """

        Available Analysis
        1.PCA
        2.ICA
        3.TSNE
        4.Classification problem -> Decision Tree
        5.Ckassification problem -> Logistic Regression 

        Exit (press any) 

    """

    print(message)
    opc = int(input('What analysis to do? '))
    ref = input('Select target for this dataset: (RANK?)')
    if(opc == 1):
        PCAnalysis(data, ref)
    elif (opc == 2):
        ICAnalysis(data, ref)
    elif (opc == 3):
        TSNEanalysis(data, ref)
    elif (opc == 4):
        res = Classification('DecisionTree', data, ref)
        if res:
            print('worked')
        else:
            print('not working')
    elif (opc == 5):
        res = Classification('Logistic', data, ref)
        if res:
            print('worked')
        else:
            print('not working')
    else:
        sys.exit(0)


