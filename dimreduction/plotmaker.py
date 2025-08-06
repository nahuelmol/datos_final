import os

def Plotter(cs, title, filepath, ref):
    #--@cs:components
    import matplotlib.pyplot as plt
    cols = [] #just column names
    for col in cs.columns:
        cols.append(col)
    plt.figure(figsize=(8,6))
    plt.scatter(cs[cols[0]], cs[cols[1]], c=cs[ref], cmap='viridis', edgecolor='k')
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.title(title)
    plt.colorbar(label=ref)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
