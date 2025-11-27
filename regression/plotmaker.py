import numpy as np
import matplotlib.pyplot as plt

def vectors_plot(X_train, y_train, filename, model):
    X = X_train.sort_index().to_numpy()
    y = y_train.to_numpy()

    pred = model.predict(X_train)
    ilok = X_train.iloc[model.support_]
    xv = X[model.support_]
    preds = np.delete(pred, -1)

    #print(xv[:,0].size)
    #print(ilok.iloc[:,0].size)

    plt.figure(figsize=(10, 6))
    plt.plot(
            xv[:,0],
            preds,
            color="g",
            lw=2,
            label="model"
            )
    for i in range(1):
        plt.scatter(
            X[model.support_][:,i],
            y[model.support_],
            facecolor=None,
            edgecolor='Green',
            s=80,
            label='data'
        )
    plt.savefig(filename, dpi=300)
    plt.close()


