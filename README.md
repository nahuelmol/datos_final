<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/count/nahuelmol/datos_final"/>
</div>

### Introduction

For the Data Laboratory final exam I had to apply PCA using the R programming language.
This respository contains the same project, but also a version implemented in Python.

### scikit-learn
The PCA is included in scikit-learn, among other methods, as a matrix decomposition algorithm. Explicitly using the skylearn.decomposition module:

```
from sklearn.decomposition import PCA
```

In scikit-learn, PCA is implemented as a transform object that takes componentes as inputs and generates others onto which the variance is better projected.

### Implemented methods

For now, the following methods were implemented:

#### Dimension reduction algorithms
* ICA
* PCA
* tSNE

#### Classification algorithms
* Logistic Regression
* Decision Tree as classifier
* Random Forest classifier
* K-nearest neighbors classifier
* Support vector classifer

#### Regression algorithms
* Linear regression
* Ridge regression
* Decision Tree regressor
* K-nearest neighbor regressor
* Support vector regressor

They are all provided by the sklearn module.
