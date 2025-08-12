<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/count/nahuelmol/datos_final"/>
</div>

### This application

For the Data Laboratory final exam I had to apply PCA using the R programming language.
This rspository contains the same project, but also a version implemented in Python and integrating other analytical methods.

This application is CLI tool that aims for direct handling of data, its processing and the looking of its corresponding outputs wether it's a plot or reports.

### scikit-learn
The used algorithms are  included in scikit-learn, specifically using sklearn. This contains classes for building machine learning models, having functions to calcultate metrics for verifying accuracy between test data and predictions made.

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

### Common commands

Let's create a new project called heisenberg (walter white)

```
cal new p:heisenberg
```

The following command applies the dimension reduction PCA algorithm. In addition, output file name and reference (which is the target colummn in the dataframe) are specified.

```
cal apply dr:<example.csv>:pca -o <pca.png> -r <reference>
```

To check current project's methods applied

```
cal check -meths
```


From the current project, specific methods can be checked. `w` stands for `where`

```
cal check -meths w pca
```

From the data directory, specific filetypes can be filter out by doing

```
cal check file -ft csv
```


Every method can be deleted on a cleaning process by typing:

```
cal clean -m pca
```

For building machine learning models, train and test data should be specified. Operator can set test file globally by doing:

```
cal set d:tt
```

where `tt` stands for test, `tn` for train and `src` for source. What follows is a questions, asking for file's name. Take into account that the file should be on the data directory. 

At the moments of buliding the model, user must choose between the setted train and test data or just splitting the source file by using `train_test_split()` function.


Projects could be also deleted by doing:

```
cal del p:heisenberg
```

or if you want to delete it all.

```
cal del p:all
```

The operator can navigates throughout different projects by doing:

```
cal switch p:pinkman
```

Other commands will be added here as the project grows

### Installation

This repository should be cloned in your local machine or just download it as a zip. Later unzip it at an specific directory.

pyinstaller is used to compile the executable:

```
pyinstaller cal.py
```

The following is copying the path to this executable at add it to enironment variables for accessing it glo0bally. 
