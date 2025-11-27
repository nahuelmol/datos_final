import numpy as np
import matplotlib.pyplot as plt

def vectors_plot(X_train, y_train, filename, model):
    X = X_train.sort_index().to_numpy()
    y = y_train.to_numpy()


    print(type(model.support_))
    print(X)
    print(y[model.support_])
    #print(y[0,1])
    
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(
        X[model.support_],
        y[model.support_],
        facecolor=None,
        edgecolor='Green',
        s=80,
        label='data'
    )
    plt.savefig(filename, dpi=300)
    plt.close()
    """


