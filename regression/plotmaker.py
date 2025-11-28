import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import plot_tree
from abss.fs import current_project

def vectors_plot(X_train, y_train, filename, model):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    X = X_train.sort_index().to_numpy()
    y = y_train.to_numpy()

    pred = model.predict(X_train)
    ilok = X_train.iloc[model.support_]
    xv = X[model.support_]
    preds = np.delete(pred, -1)

    plt.figure(figsize=(10, 6))
    plt.plot(
            X[model.support_][:,0],
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
    plt.savefig(filepath, dpi=300)
    plt.close()


def knnr_plot(X_train, y_train, filename, model):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)

    plt.figure(figsize=(10, 6))
    plt.scatter(X_train, y_train, color='darkorange', label='data')
    plt.plot(X_test, y_pred, color='navy', label=f'KNN Regression (k={n_neighbors})')
    plt.xlabel('Feature (X)')
    plt.ylabel('Target (y)')
    plt.title('K-Nearest Neighbors Regression')
    plt.legend()
    plt.grid(True)
    plt.savefig(filepath, dpi=300)
    plt.close()

def dtree_plot(X_train, y_train, filename, model):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)

    plt.figure(figsize=(12,8))
    plot_tree(model, filled=True, feature_names=['Feature_X'], rounded=True, fontsize=10)
    plt.title("Decision Tree Regressor")
    plt.savefig(filepath, dpi=300)
    plt.close()

def ridge_r_plot(pred, X_train, y_train, filename, model):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    plt.plot(X_train, y_train, label="True signal", linewidth=2)
    plt.scatter(
        X_train.iloc[:,0],
        y_train,
        color="black",
        label="Noisy measurements",
    )
    pred_wt = model.predict(X_train)
    plt.plot(X_train, pred_wt, label="Ridge regression")
    plt.legend()
    plt.xlabel("data")
    plt.ylabel("target")
    plt.savefig(filepath, dpi=300)
    plt.close()

def linear_plot(X_train, y_train, filename, model):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    plt.scatter(X_test, y_test, color='black', label='Actual data')
    plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Linear Regression')
    plt.xlabel('Feature')
    plt.ylabel('Target')
    plt.title('Scikit-learn Linear Regression')
    plt.legend()
    filename = 'linearRegression'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
