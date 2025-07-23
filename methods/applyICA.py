import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FastICA
from .plotmaker import Plotter

def ICAnalysis(data, ref):
    #the same, select numerical columns (an what I aim to separate?)
    target = data.pop(ref)
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != ref:
                cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)

    n_components = int(input('How many components you want?'))
    ica = FastICA(n_components=n_components, random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ICs  = pd.DataFrame(x_ica, columns=['IC1', 'IC2'])
    result  = pd.concat([target, ICs], axis=1)
    print(ICs)

    Plotter(result, 'ICA - Independent Components Analysis')
