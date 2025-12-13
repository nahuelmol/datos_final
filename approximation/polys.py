from scipy.interpolate import lagrange
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#def Lagrange(cmd):
def prove():
    path            = "../data/EMI1.txt"
    df              = pd.read_csv(path, sep='\t')
    df['Ip_val']    = df['Ip'] * df['XI']
    df['Op_val']    = df['Op'] * df['XO']

    x = df['Pro.']
    y = df['Ip_val']

    poly = lagrange(x, y)
    x_trained = np.linspace(min(x), max(x), 500)
    y_trained = poly(x_trained)

    plt.figure()
    plt.plot(x, y, 'o', label='Data')
    plt.plot(x_trained, y_trained, '-', label='Lagrange')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('output.png', bbox_inches='tight', dpi=300)
    plt.close()

prove()
