
def DecisionTree(data):
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.metrics import accuracy_score

    data = data.query("POS.isin(('C', 'G'))")

    #training dataset
    X = data[['SPG', 'APG', 'PPG', 'BPG']]
    Y = (data['POS'] == 'C') # =0 if C, =1 if G 

    TREE = DecisionTreeClassifier(max_depth=1).fit(X, Y) #finds the bias
    plot_tree(TREE)
    predictions = TREE.predict(X)
    predictions[3]

    accuracy_score(Y, TREE.predict(X))
    

def Logistic(data):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import make_classification

    X = data[['APG', 'SPG', 'BPG', 'PPG']] #select features
    y = data['G'] #target variable, guardian

    #X, y = make_classification(n_samples=100, 
    #                           n_features=2, 
    #                           n_informative=2, 
    #                           n_redundant=0, 
    #                           random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    cr = classification_report(y_test, y_pred)
    mc = model.coef_
    mi = model.intercept_
    cm = model.confusion_matrix(y_test, y_pred)
    REPORT = {
        'model_coef': mc,
        'model_intercept': mi,
        'confusion_matrix': cm,
        'classification_report': cr
    }

