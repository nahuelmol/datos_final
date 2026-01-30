<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/datos_final"/>
  <img src="https://img.shields.io/github/languages/count/nahuelmol/datos_final"/>
</div>

### This application

For the Data Laboratory final exam I had to apply PCA using the R programming language.
This rspository contains the same project, but also a version implemented in Python and extending by adding other analytical methods.

This application is a CLI tool that aims for:
* handling raw data
* data cleaning
* data processing
* data visualization through plots or data-file outputs

### Libraries used

* Sklearn: provides machine learning algorithms making possible to build classification and regression models, implementing unsupervised techniques.
* Scipy: provides scientific algorithms needed for statistics and signal processing. It makes possible to build polynomials that better fits a set of values.
* Numpy: introduce multi dimensional arrays and a set of mathematical functions to operate on these ndarrays.
* Pandas: allows to work with external data files in python which becomes very powerful at combining it with numpy functionalities.

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

### Polynomial algorithms
* Lagrange
* Chebyshev
* Taylor (in progress)

### Common commands

Let's create a new project called heisenberg (walter white)

```
cal new p:heisenberg
```

Later, for setting an specific source data file:

```
cal set d:src
```

Global variables or labels can be setted for exploratory univariate analysis like building histograms, boxplots or printing dispersion statistics.

```
cal set g:var
```

```
cal set g:lab
```

```
cal set g:histo_var
```

Once a data source is selected, its variables can be observed by using list. For type, n stands for numerical and c for categorical. A white space includes all variables. Once variables are listed, any can be choosen to fill the var or histo_var (which cannot be categorical) field.

```
cal list vars <type>
```

### Exploratory analysis

For exploratory analysis xp command is used. If any type of analysis is specified it executes everyone as long as variables are setted at the manifest.json. Available types are boxplot, histograms, correlation matrix, dispersion metrics, and cateogorical variables. Use the help command to learn the code that stands for the the mentioned analysis.

```
cal xp <type>
```

### Dimension reduction algorithms

The following command applies the dimension reduction PCA algorithm taking the source file previously setted:

```
cal app dr:pca -r <reference>
```

Alternatively, output filename and reference (which is the target colummn in the dataframe) can be specified in the same command:

```
cal app dr:<example.csv>:pca -o <pca.png> -r <reference>
```

### Classification models

For classification using Logistic model:

```
cal app c:l -r <reference>
```

### Regression models

This is analogous to the previous one:

```
cal app r:svr -r <reference>
```

### Approxiamtion with or without polynomials

Specific polynomails can be used to aproximate to the data.

```
cal app a:l
```

`l` stands for lagrange, `c` for chebyschev. Besides that, `s` stands for lines and allows the plotting of raw data. Previously, for EMI data, profiles must be setted using `-`

### Checking

To check the applied current project's methods or the models built, `ch` is used (which stands for check) as follows:

```
cal ch meths
cal ch mods
cal ch exps
cal ch pols
```

The target mods, meths, exps and pols work under the same logic. From the current project, specific methods can be checked. `w` stands for `where` conditioning a type group and `is` signs an specific method.

```
cal ch meths w pca
```

```
cal ch meths w pca is 1
```

From the data directory, specific filetypes can be filter out by doing

```
cal ch file -ft csv
```

### Cleaning

Every method and models can be deleted on a cleaning process by typing the `cl` command that stands for clean. The use is the same as for `ch`. 

```
cal cl meths w pca
```

```
cal cl meths w pca is 1
```

```
cal cl pols
```

### Setting datasets

For building machine learning models, train and test data should be specified or the program will use src specified. Operator can set test file globally by doing:

```
cal set d:tt
```

where `tt` stands for test, `tn` for train and `src` for source. What follows is a questions, asking for target file's name. Take into account that the file should be on the `data` directory. 

At the moment of buliding the model, user must choose between the setted train and test data or just splitting the source file by using `train_test_split()` function that applies a `test_size=0.2` unless the key `-ts` is included followed by any test size required.

### Projects management

Projects could be also deleted by doing:

```
cal del p:heisenberg
```

or if you want to delete it all.

```
cal del p:all
```

Also, produced plots as images can be delted:

```
cal del o:all 
```

The operator can navigates throughout different projects by doing:

```
cal switch p:pinkman
```

Other commands will be added here as the project grows

### Plotting with gnuplot

Located in the "data" directory, enter the gnuplot assitant:

```
gnuplot
```

Then enter the following commands:

```
set xlabel "Longitud"
set ylabel "Latitud"
set zlabel "REa"
set datafile separator ','
```

Later, a 3D scatter plot can be built:

```
splot "Grid" using 6:5:4 with points pt 7 ps 1 notitle
```

And also, a surface plot:

```
set hidden3d
set pm3d at s
set view 60, 30
set dgrid3d 50, 50, 2
splot "Grid" using 6:5:4 with pm3d
```


### Installation

This repository should be cloned in your local machine or just download it as a zip. Later unzip it at an specific directory. Then use `pip` to all install libraries needed.

```
pip install -r requirements.txt
```

pyinstaller is used to compile the executable:

```
pyinstaller cal.py
```

The following is to paste the path to this executable in environment variables. This way the utility can be used globally. 
