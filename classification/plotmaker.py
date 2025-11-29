
import os
import numpy as np
import matplotlib.pyplot as plt

from abss.fs import current_project

def logistic_regression_plot(X, y, X_test, y_test, model, filename, clase):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    x_min, x_max = X_test.iloc[:, 0].min() - 1, X_test.iloc[:, 0].max() + 1
    y_min, y_max = X_test.iloc[:, 1].min() - 1, X_test.iloc[:, 1].max() + 1
    xx, yy = np.meshgrid(
            np.arange(x_min, x_max, 0.02),
            np.arange(y_min, y_max, 0.02))

    grid_points = np.zeros((xx.size, X_test.shape[1]))
    grid_points[:] = X_test.mean().values
    grid_points[:,0] = xx.ravel()
    grid_points[:,1] = yy.ravel()
    Z = model.predict_proba(grid_points)
    Z_class = Z[:, clase]
    Z_class = Z_class.reshape(xx.shape)

    le = LabelEncoder()
    y_num = le.fit_transform(y_test)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z_class, alpha=0.8, cmap=plt.cm.RdBu)
    plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_num, cmap=plt.cm.RdBu, edgecolor='k', s=20)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.title("Logistic Regression Decision Boundary")

    plt.savefig(filepath, dpi=300)
    plt.close()

def confusion_matrix_plot(cm, classes, filename):
    pname = current_project(['project_name'])
    filepath = 'prs\{}\outputs\{}'.format(pname, filename)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    disp.plot(cmap="Blues", values_format='d')
    plt.savefig(filepath, dpi=300)
    plt.close()
