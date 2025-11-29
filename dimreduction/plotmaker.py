import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay
from abss.fs import current_project

def Plotter(cs, title, filename, ref):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    #--@cs:components
    cols = [] #just column names
    for col in cs.columns:
        cols.append(col)
    plt.figure(figsize=(8,6))
    plt.scatter(cs[cols[0]], cs[cols[1]], c='r', cmap='viridis', edgecolor='k')
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.title(title)
    plt.colorbar(label=ref)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()


