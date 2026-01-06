import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt

from scipy.interpolate import lagrange, approximate_taylor_polynomial
from scipy.special import chebyt
from numpy.polynomial.polynomial import Polynomial
from numpy.polynomial import chebyshev as cheby
from datetime import datetime
from pathlib import Path

from abss.fs import current_project, taken
from abss.data_setter import get_data

class Polymaker:
    def __init__(self, cmd):
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath, '\t')
        filename = datapath.split('\\')[-1]

        self.firstday   = [5,6]
        self.secndday   = [1,2,3,4]
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

        self.cond_ap    = np.sqrt(self.ip.pow(2) + self.op.pow(2))
        self.rest_ap    = self.cte_rest / self.cond_ap

        self.rest_ap.name = 'RA'
        self.cond_ap.name = 'CA'
        self.ip.name    = 'IP'
        self.op.name    = 'OP'

        self.poly_type  = cmd.method
        self.poly_ip    = None 
        self.poly_op    = None 
        self.poly_ra    = None 
        self.poly_ca    = None 

        self.output_ip  = None
        self.output_op  = None
        self.output_ra  = None
        self.output_ca  = None

        self.coeffs_ip  = None
        self.coeffs_op  = None
        self.coeffs_ra  = None
        self.coeffs_ca  = None

        self.n          = None
        self.REPORT     = {}
        self.filename   = {}

        self.framed_locs= None

    def build_poly(self):
        if self.poly_type == 'l':
            self.poly_name = 'lagrange'
            self.n = taken('polys', self.poly_name)
            self.Lagrange()
        elif self.poly_type == 'c':
            self.poly_name = 'chebyshev'
            self.n = taken('polys', self.poly_name)
            self.Chebyshev()
        elif self.poly_type == 't':
            self.poly_name = 'taylor'
            self.n = taken('polys', self.poly_name)
            self.Taylor()
        else:
            print('not recognized poly')
            return False
        self.output_ip  = self.poly_ip(self.x_trained)
        self.output_op  = self.poly_op(self.x_trained)
        self.output_ra  = self.poly_ra(self.x_trained)
        self.output_ca  = self.poly_ca(self.x_trained)

        self.coeffs_ip  = self.poly_ip.coeffs
        self.coeffs_op  = self.poly_op.coeffs
        self.coeffs_ra  = self.poly_ra.coeffs
        self.coeffs_ca  = self.poly_ca.coeffs
        return True

    def Lagrange(self):
        self.coeffs_ip  = np.polyfit(self.x, self.ip, 20)
        self.coeffs_op  = np.polyfit(self.x, self.op, 20)
        self.coeffs_ra  = np.polyfit(self.x, self.rest_ap, 20)
        self.coeffs_ca  = np.polyfit(self.x, self.cond_ap, 20)

        self.poly_ip    = np.poly1d(self.coeffs_ip)
        self.poly_op    = np.poly1d(self.coeffs_op)
        self.poly_ra    = np.poly1d(self.coeffs_ra)
        self.poly_ca    = np.poly1d(self.coeffs_ca)

        files = {
            'basic': 'scatter_lagrange_{}.png'.format(self.n),
            'polys': 'polys_lagrange_{}.png'.format(self.n),
            'complete': 'complete_lagrange_{}.png'.format(self.n),
        }
        self.REPORT = {
            'poly':'lagrange',
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files

    def Taylor(self):
        x_0 = 0.0
        grade = 4
        scale = 1.0
        self.poly_ip = approximate_taylor_polynomial(self.ip, x_0, grade, scale=scale)
        self.poly_op = approximate_taylor_polynomial(self.op, x_0, grade, scale=scale)

        files = {
            'basic': 'scatter_taylor_{}.png'.format(self.n),
            'polys': 'polys__{}.png'.format(self.n),
        }
        self.REPORT = {
            'poly':'taylor',
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files

    def Chebyshev(self):
        grade = 20 
        self.coeffs_ip  = cheby.chebfit(self.x, self.ip, grade)
        self.coeffs_op  = cheby.chebfit(self.x, self.op, grade)
        self.coeffs_ra  = cheby.chebfit(self.x, self.rest_ap, grade)
        self.coeffs_ca  = cheby.chebfit(self.x, self.cond_ap, grade)

        cheb2poly_ip    = cheby.cheb2poly(self.coeffs_ip)
        cheb2poly_op    = cheby.cheb2poly(self.coeffs_op)
        cheb2poly_ra    = cheby.cheb2poly(self.coeffs_ra)
        cheb2poly_ca    = cheby.cheb2poly(self.coeffs_ca)
        self.poly_ip    = np.poly1d(cheb2poly_ip[::-1])
        self.poly_op    = np.poly1d(cheb2poly_op[::-1])
        self.poly_ra    = np.poly1d(cheb2poly_ra[::-1])
        self.poly_ca    = np.poly1d(cheb2poly_ca[::-1])

        files = {
            'basic': 'scatter_chebyshev_{}.png'.format(self.n),
            'polys': 'polys_chebyshev_{}.png'.format(self.n),
            'complete':'complete_chebyshev_{}.png'.format(self.n),
        }
        self.REPORT = {
            'poly':'chebyshev',
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
        return True
    
    def transf_locs(self):
        new_lat = None
        new_lon = None
        for idx, row in self.framed_locs.iterrows():
            print('{} - {}'.format(row['Lat'], row['Lon']))
            if self.nprofile in self.firstday:
                if selflocs.iloc[idx-1] == None:
                    next_lon = abs(self.framed_locs.iloc[idx+1]['Lon'])
                    next_lat = abs(self.framed_locs.iloc[idx+1]['Lat'])
                    curr_lon = abs(row['Lon'])
                    curr_lat = abs(row['Lat'])
                    if next_lon < curr_lon:
                        if math.copysign(1, row['Lon']) == -1.0:
                            new_lon = row['Lon'] - 0.00018
                        elif math.copysign(1, row['Lon']) == 1.0:
                            new_lon = row['Lon'] + 0.00018
                    else:
                        if math.copysign(1, row['Lon']) == -1.0:
                            new_lon = row['Lon'] + 0.00018
                        elif math.copysign(1, row['Lon']) == 1.0:
                            new_lon = row['Lon'] - 0.00018

                    if next_lat < curr_lat:
                        if math.copysign(1, row['Lat']) == -1.0:
                            new_lat = row['Lat'] - 0.00018
                        elif math.copysign(1, row['Lat']) == 1.0:
                            new_lat = row['Lat'] + 0.00018
                    else:
                        if math.copysign(1, row['Lat']) == -1.0:
                            new_lon = row['Lat'] + 0.00018
                        elif math.copysign(1, row['Lat']) == 1.0:
                            new_lon = row['Lat'] - 0.00018

            elif self.nprofile in self.secndday:
                if self.framed_locs.iloc[idx+1] == None:
                    prev_lon = abs(self.framed_locs.iloc[idx-1]['Lon'])
                    prev_lat = abs(self.framed_locs.iloc[idx-1]['Lat'])
                    curr_lon = abs(row['Lon'])
                    curr_lat = abs(row['Lat'])
                    if prev_lon < curr_lon:
                        if math.copysign(1, row['Lon']) == -1.0:
                            new_lon = row['Lon'] - 0.00018
                        elif math.copysign(1, row['Lon']) == 1.0:
                            new_lon = row['Lon'] + 0.00018
                    else:
                        if math.copysign(1, row['Lon']) == -1.0:
                            new_lon = row['Lon'] + 0.00018
                        elif math.copysign(1, row['Lon']) == 1.0:
                            new_lon = row['Lon'] - 0.00018

                    if prev_lat < curr_lat:
                        if math.copysign(1, row['Lat']) == -1.0:
                            new_lon = row['Lat'] - 0.00018
                        elif math.copysign(1, row['Lat']) == 1.0:
                            new_lon = row['Lat'] + 0.00018
                    else:
                        if math.copysign(1, row['Lat']) == -1.0:
                            new_lon = row['Lat'] + 0.00018
                        elif math.copysign(1, row['Lat']) == 1.0:
                            new_lon = row['Lat'] - 0.00018

                else:
                    new_lat = (row['Lat'] + self.framed_locs.iloc[idx+1]['Lat']) / 2
                    new_lon = (row['Lon'] + self.framed_locs.iloc[idx+1]['Lon']) / 2
            self.framed_locs.iloc[idx]['Lat'] = new_lat
            self.framed_locs.iloc[idx]['Lon'] = new_lon

    def add_locs(self):
        nfirst  = self.Stats.iloc[0] - 1
        nlastt  = (self.Stats.iloc[-1])
        locs    = pd.read_csv("data/locations.dat")

        self.framed_locs = locs.iloc[nfirst:nlastt]
        self.transf_locs()
        lat     = self.framed_locs['Lat'].reset_index()
        lon     = self.framed_locs['Lon'].reset_index()

        ready = pd.concat([self.Stats, self.ip, self.op, self.rest_ap, lat['Lat'], lon['Lon']], axis=1)
        output_name = "data/Profile {}".format(self.nprofile)
        ready.to_csv(output_name, index=False)

    def build_grid(self):
        p = Path("data")
        profs = list(p.rglob(f'Profile*'))
        locs = pd.read_csv("data/locations.dat")
        n = locs.shape[0]
        my_pds = []
        for prof in profs:
            df = pd.read_csv(prof)
            my_pds.append(df)
        comb = pd.concat(my_pds, ignore_index=True)
        output_name = "data/Grid"
        comb.to_csv(output_name, index=False)

    def basic_plot(self):
        pname = current_project(['project_name'])
        filepath = 'prs\{}\outputs\{}'.format(pname, self.filename['basic'])
        plt.figure()
        plt.plot(self.x, self.ip, 'o', label='Data')
        plt.plot(self.x, self.op, 'o', label='Data')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def polys_plot(self):
        pname = current_project(['project_name'])
        filepath = 'prs\{}\outputs\{}'.format(pname, self.filename['polys'])
        plt.figure()
        #plt.plot(self.x_trained, Polynomial(self.coeffs_ip[::-1])(self.x_trained), label='Polynomial Ip')
        #plt.plot(self.x_trained, Polynomial(self.coeffs_op[::-1])(self.x_trained), label='Polynomial Op')
        plt.plot(self.x_trained, self.output_ip, '-', label='Lagrange ip')
        plt.plot(self.x_trained, self.output_op, '-', label='Lagrange op')
        plt.ylim(-80, 80)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def complete_plot_ipop(self):
        pname = current_project(['project_name'])
        filepath = 'prs\{}\outputs\{}'.format(pname, self.filename['complete'])
        plt.figure()
        plt.plot(self.x_trained, self.output_ip, '-', label='Lagrange ip')
        plt.plot(self.x_trained, self.output_op, '-', label='Lagrange op')
        plt.plot(self.x, self.ip, 'o', label='Data ip')
        plt.plot(self.x, self.op, 'o', label='Data op')
        plt.ylim(-80, 80)
        plt.xlabel('x(prog)')
        plt.ylabel('y(cond)')
        plt.legend()
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def complete_plot_ap(self, which):
        pname = current_project(['project_name'])
        filepath = 'prs\{}\outputs\{}'.format(pname, self.filename['complete'])
        plt.figure()
        output = None
        poly_label = ''
        datarange = 10
        if which == 'R':
            output      = self.output_ra
            poly_label  = 'Resistivity'
            scatter = self.rest_ap
            datarange = 5
        elif which == 'C':
            output      = self.output_ca
            poly_label  = 'Conductivity'
            scatter = self.cond_ap
            datarange = 80
        scatter_label = 'Data'

        plt.plot(self.x_trained, output, '-', label=poly_label)
        plt.plot(self.x, scatter, 'o', label=scatter_label)
        plt.ylim(-datarange, datarange)
        plt.xlabel('x(prog)')
        plt.ylabel('y(cond)')
        plt.title('Profile {}'.format(self.nprofile))
        plt.legend()
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()
