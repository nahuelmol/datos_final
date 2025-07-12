
For the Data Laboratory final exam I had to apply PCA using the R programming language.
This respository contains the same project, but also a version implemented in Python.

### scikit-learn
The PCA in scikit learn is included, among other methods, as a matrix decomposition algorithm. Explicitly using the skylearn.decomposition module:

```
from sklearn.decomposition import PCA
```

In scikit-learn, PCA is implemented as a transform object that takes componentes as inputs and generates others onto which the variance is better projected.
