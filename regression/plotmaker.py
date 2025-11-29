import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import plot_tree
from abss.fs import current_project

class Plot():
    def __init__(self, X_train, y_train, filename, model):
        pname = current_project(['project_name'])
        self.filepath = 'prs\{}\outputs\{}'.format(pname, filename)
        self.model = model
        self.X_train = X_train.sort_index()
        self.y_train = y_train.sort_index()
        self.pred_train = self.model.predict(self.X_train) 

    def vectors(self):
        pname = current_project(['project_name'])
        filepath = 'prs\{}\outputs\{}'.format(pname, filename)

        X = self.X_train.iloc[model.support_]
        preds = np.delete(self.pred_train, -1)

        plt.figure(figsize=(10, 6))
        plt.plot(
                X[:,0],
                preds,
                color="g",
                lw=2,
                label="model"
                )
        for i in range(1):
            plt.scatter(
                X[:,i],
                y[model.support_],
                facecolor=None,
                edgecolor='Green',
                s=80,
                label='data'
            )
        plt.savefig(self.filepath, dpi=300)
        plt.close()

    def knnr(self, X_train, y_train, filename, model):

        plt.figure(figsize=(10, 6))
        plt.scatter(self.X_train, self.y_train, color='darkorange', label='data')
        #plt.plot(self.X_train, self.pred_train, color='navy', label=f'KNN Regression (k={n_neighbors})')
        plt.xlabel('Feature (X)')
        plt.ylabel('Target (y)')
        plt.title('K-Nearest Neighbors Regression')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.filepath, dpi=300)
        plt.close()

    def dtree(self):

        plt.figure(figsize=(12,8))
        plot_tree(self.model, filled=True, feature_names=['Feature_X'], rounded=True, fontsize=10)
        plt.title("Decision Tree Regressor")
        plt.savefig(self.filepath, dpi=300)
        plt.close()

    def ridge(self):
        plt.plot(self.X_train, self.y_train, label="True signal", linewidth=2)
        plt.scatter(
            self.X_train.iloc[:,0],
            self.y_train,
            color="black",
            label="Noisy measurements",
        )
        pred_wt = self.model.predict(self.X_train)
        plt.plot(self.X_train, pred_wt, label="Ridge regression")
        plt.legend()
        plt.xlabel("data")
        plt.ylabel("target")
        plt.savefig(self.filepath, dpi=300)
        plt.close()

    def linear(self):
        plt.scatter(
                self.X_train.iloc[:,0], 
                self.y_train, 
                color='black', 
                label='Actual data')
        plt.plot(
                self.X_train.iloc[:,0], 
                self.pred_train, 
                color='blue', 
                linewidth=3, 
                label='Linear Regression Model')
        plt.xlabel('Feature')
        plt.ylabel('Target')
        plt.title('Scikit-learn Linear Regression')
        plt.legend()
        filename = 'linearRegression'
        plt.savefig(self.filepath, dpi=300, bbox_inches='tight')
        plt.close()
