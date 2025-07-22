

def IPCAnalysis(data):
    #the same, select numerical columns (an what I aim to separate?)
    features = data[['APG', 'SPG', 'BPG', 'PPG']]
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(features)

    from sklearn.decomposition import FastICA
    ica = FastICA(n_components=2, random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ica_df  = pd.DataFrame(x_ica, columns=['IC1', 'IC2'])
    result  = pd.concat([df, ica_df], axis=1)

    Plotter(result, 'ICA - Independent Components Analysis')
