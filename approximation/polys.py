import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt

from scipy.interpolate import lagrange, approximate_taylor_polynomial
from scipy.special import chebyt
from datetime import datetime
from pathlib import Path

from abss.fs import current_project, take_n
from abss.data_setter import get_data

class Polynomial:
    def __init__(self, cmd):
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath, '\t')
        filename = datapath.split('\\')[-1]

        self.mhu        = 0.00000125
        self.s          = 40
        self.w          = 2 * math.pi * 3600
        self.cte_rest   = self.mhu * self.w * (math.pow(self.s, 2)) /4

        self.Stats      = data['St.']
        self.nprofile   = filename[3]
        self.x          = data['Pro.']
        self.ip         = data['Ip'] * data['XI']
        self.op         = data['Op'] * data['XO']
        self.x_trained  = np.linspace(min(self.x), max(self.x), 500)
        self.nrows      = data.shape[0]

        module = np.sqrt(self.ip.pow(2) + self.op.pow(2))
        self.rest_ap    = self.cte_rest / module 

        self.rest_ap.name = 'RA'
        self.ip.name    = 'IP'
        self.op.name    = 'OP'

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

    def create_locs(self):
        loc_path = "data/locations.dat"
        if(os.path.exists(loc_path)):
            return True
        path    = "data/Ubicacion_slingram_camp2.dat"
        lat = []
        lon = []
        i   = 0
        with open(path, 'r') as f:
            for line in f:
                if(i != 0):
                    mylist = line.split(" ")
                    lat.append(mylist[0])
                    lon.append(mylist[1])
                i = i+1
        lat = pd.Series(lat)
        lon = pd.Series(lon)
        ready   = pd.DataFrame({
            'Lat': lat,
            'Lon': lon
        })
        ready.to_csv('data/locations.dat', index=False)
    
    def add_locs(self):
        nfirst  = self.Stats.iloc[0]
        nlastt  = (self.Stats.iloc[-1] + 1)
        locs    = pd.read_csv("data/locations.dat")

        framed_locs = locs.iloc[nfirst:nlastt]
        lat     = framed_locs['Lat'].reset_index()
        lon     = framed_locs['Lon'].reset_index()

        ready = pd.concat([self.Stats, self.ip, self.op, self.rest_ap, lat['Lat'], lon['Lon']], axis=1)
        output_name = "data/Profile {}".format(self.nprofile)
        ready.to_csv(output_name, index=False)

    def build_grid(self):
        p = Path("data")
        profs = list(p.rglob(f'Profile*'))
        locs = pd.read_csv("data/locations.dat")
        n = locs.shape[0]
        #a = np.zeros(n, 5)
        my_pds = []
        for prof in profs:
            df = pd.read_csv(prof)
            my_pds.append(df)
        comb = pd.concat(my_pds, ignore_index=True)
        output_name = "data/Grid"
        comb.to_csv(output_name, index=False)

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

