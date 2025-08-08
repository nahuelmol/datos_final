import os
import matplotlib.pyplot as plt

def Plotter(cs, title, filepath, ref):
    #--@cs:components
    cols = [] #just column names
    for col in cs.columns:
        cols.append(col)
    plt.figure(figsize=(8,6))
    plt.scatter(cs[cols[0]], cs[cols[1]], c=cs[ref], cmap='viridis', edgecolor='k')
    print('0: ', cols[0])
    print('1: ', cols[1])
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.title(title)
    plt.colorbar(label=ref)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

