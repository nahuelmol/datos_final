
def Plotter(cs, title):
    #--@cs:components
    import matplotlib.pyplot as plt
    filepath = 'output.png'
    cols = [] #just column names
    for col in cs.columns:
        cols.append(col)
    plt.figure(figsize=(8,6))
    #plt.scatter(pcs['pc1'], pcs['pc2'], c=pcs['RANK'], cmap='viridis', edgecolor='k')
    plt.scatter(cs[cols[0]], cs[cols[1]], c=cs['RANK'], cmap='viridis', edgecolor='k')
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.title(title)
    plt.colorbar(label='RANK')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
