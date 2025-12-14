import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.interpolate import lagrange, approximate_taylor_polynomial
from scipy.special import chebyt

from abss.fs import current_project
from abss.data_setter import get_data

def Lagrange(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath, '\t')

    x   = data['Pro.']
    ip  = data['Ip'] * data['XI']
    op  = data['Op'] * data['XO']

    poly_ip = lagrange(x, ip)
    poly_op = lagrange(x, op)
    x_trained = np.linspace(min(x), max(x), 500)
    output_ip = poly_ip(x_trained)
    output_op = poly_op(x_trained)

    plt.figure()
    plt.plot(x, ip, 'o', label='Data')
    plt.plot(x, op, 'o', label='Data')
    plt.plot(x_trained, output_ip, '-', label='Lagrange ip')
    plt.plot(x_trained, output_op, '-', label='Lagrange op')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('output.png', bbox_inches='tight', dpi=300)
    plt.close()

def Taylor(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath, '\t')
    x_0 = 0
    grade = 4
    x   = data['Pro.']
    ip  = data['Ip'] * data['XI']
    op  = data['Op'] * data['XO']
    poly_ip = approximate_taylor_polynomial(ip, x_0, grade, scale=1.0)
    poly_op = approximate_taylor_polynomial(op, x_0, grade, scale=1.0)

    x_vals = np.linspace(min(x), max(x), 400)
    plt.plot(x_vals, f(x_vals), label='f(x)=sin(x)')
    plt.plot(x_vals, poly(x_vals), label='Taylor')
    plt.title('Taylor approximation')
    plt.legend()
    plt.grid(True)
    plt.show()

def Chebyshev(cmd):
    datapath = current_project(['datapath','src'])
    res, data = get_data(datapath, '\t')
    data['Ip_val']    = data['Ip'] * data['XI']
    data['Op_val']    = data['Op'] * data['XO']

    x = data['Pro.']
    y = data['Ip_val']
    T2 = chebyt(2)
    x_axis = np.linspace(min(x),max(x),500)
    y = T2(x)

    filepath = filename
    plt.plot(x, y, label='Chebyshev')
    plt.title('Chebyshev approximation')
    plt.legend()
    plt.grid(True)
    plt.savefig(filepath, dpi=300)
    plt.close()


