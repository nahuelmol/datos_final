import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.interpolate import lagrange, approximate_taylor_polynomial
from scipy.special import chebyt
from datetime import datetime

from abss.fs import current_project, take_n
from abss.data_setter import get_data

class Polynomial:
    def __init__(self, cmd):
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath, '\t')
        filename = datapath.split('\\')[-1]

        self.Stats  = data['St.']
        self.nprofile  = filename[3]
        self.x      = data['Pro.']
        self.ip     = data['Ip'] * data['XI']
        self.op     = data['Op'] * data['XO']
        self.x_trained = np.linspace(min(self.x), max(self.x), 500)
        self.nrows = data.shape[0]

        self.poly_type = cmd.method
        self.poly_ip = None 
        self.poly_op = None 
        self.output_ip = None
        self.output_op = None
        self.n = None
        self.REPORT = {}
        self.filename = None

    def build_poly(self):
        if(self.poly_type == 'l'):
            self.poly_name = 'lagrange'
        elif (self.poly_type == 'c'):
            self.poly_name = 'chebyshev'
        elif (self.poly_type == 't'):
            self.poly_name = 'talor'
        self.n = take_n('polys', self.poly_name)
        if self.poly_type == 'l':
            self.Lagrange()
            self.output_ip = self.poly_ip(self.x_trained)
            self.output_op = self.poly_op(self.x_trained)
            return True
        elif self.poly_type == 'c':
            self.Chebyshev()
            self.output_ip = self.poly_ip(self.x_trained)
            self.output_op = self.poly_op(self.x_trained)
            return True
        elif self.poly_type == 't':
            self.Taylor()
            self.output_ip = self.poly_ip(self.x_trained)
            self.output_op = self.poly_op(self.x_trained)
            return True
        else:
            print('not recognized poly')
            return False

    def Lagrange(self):
        self.poly_ip = lagrange(self.x, self.ip)
        self.poly_op = lagrange(self.x, self.op)

        files = {
            'basic': 'scatter_lagrange_{}.png'.format(self.n),
        }
        self.REPORT = {
            'polys':'taylor',
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files


    def Taylor(self):
        x_0 = 0
        grade = 4
        self.poly_ip = approximate_taylor_polynomial(self.ip, x_0, grade, scale=1.0)
        self.poly_op = approximate_taylor_polynomial(self.op, x_0, grade, scale=1.0)

        files = {
            'basic': 'scatter_taylor_{}.png'.format(self.n),
        }
        self.REPORT = {
            'polys':'taylor',
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files

    def Chebyshev(sefl):
        T2 = chebyt(2)
        y = T2(self.x_trained)

        files = {
            'basic': 'scatter_taylor_{}.png'.format(self.n),
        }
        self.REPORT = {
            'polys':'chebyshev',
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files

    def add_locs(self):
        path    = "data/Ubicacion_slingram_camp2.dat"
        nfirst  = self.Stats.iloc[0]
        nlastt  = self.Stats.iloc[-1]
        n       = nlastt - (nfirst - 1)
        data    = np.zeros((n, 2))
        i = 0
        with open(path, 'r') as f:
            for line in f:
                if(i != 0):
                    mylist = line.split(" ")
                    data[i-1, 0] = mylist[0]
                    data[i-1, 1] = mylist[1]
                if(i == n):
                    break
                i = i + 1

        df      = pd.DataFrame(data, columns=['Lon', 'Lat'])
        ready   = pd.DataFrame({
            'St.': self.Stats,
            'Ip':  self.ip,
            'Op':  self.op,
            'Lat': df['Lat'],
            'Lon': df['Lon']
        })
        output_name = "Profile {}".format(self.nprofile)
        ready.to_csv(output_name, index=False)

    def basic_plot(self):
        plt.figure()
        plt.plot(self.x, self.ip, 'o', label='Data')
        plt.plot(self.x, self.op, 'o', label='Data')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(self.filename['basic'], bbox_inches='tight', dpi=300)
        plt.close()

    def polys_plot(self):
        plt.figure()
        plt.plot(self.x_trained, self.output_ip, '-', label='Lagrange ip')
        plt.plot(self.x_trained, self.output_op, '-', label='Lagrange op')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(self.filename['basic'], bbox_inches='tight', dpi=300)
        plt.close()

    def complete_plot(self):
        plt.figure()
        plt.plot(self.x_trained, self.output_ip, '-', label='Lagrange ip')
        plt.plot(self.x_trained, self.output_op, '-', label='Lagrange op')
        plt.plot(self.x, self.ip, 'o', label='Data')
        plt.plot(self.x, self.op, 'o', label='Data')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(self.filename['basic'], bbox_inches='tight', dpi=300)
        plt.close()

