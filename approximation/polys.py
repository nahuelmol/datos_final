import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import plotly as px
import seaborn as sns
import folium

from scipy.interpolate import lagrange, approximate_taylor_polynomial
from scipy.special import chebyt
from scipy.spatial import ConvexHull, Delaunay
from scipy.stats import gaussian_kde
from numpy.polynomial.polynomial import Polynomial
from numpy.polynomial import chebyshev as cheby
from datetime import datetime
from pathlib import Path
from matplotlib.path import Path
from matplotlib.colors import LogNorm

from abss.fs import current_project, taken
from abss.data_setter import get_data
from abss.story import add
from folium.plugins import HeatMap

class Polymaker:
    def __init__(self, cmd):
        self.pname = current_project(['project_name'])
        datapath = current_project(['datapath','src'])
        res, data = get_data(datapath, '\t')
        filename = datapath.split('\\')[-1]

        self.linetype   = cmd.linetype

        self.firstday   = [12, 13]
        self.secndday   = [1,2,3,4,5,6,7,8,9,10,11]
        self.mhu        = 0.00000125
        self.s          = 40
        self.w          = 2 * math.pi * 3600
        self.cte_rest   = self.mhu * self.w * (math.pow(self.s, 2)) /4

        self.profile    = data['P']
        self.stats      = data['St.']
        self.nplanilla  = filename[3]
        self.nprofile   = None 
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
        elif self.poly_type == '-':
            self.set_profile()
            return True
        elif self.poly_type == 's':
            self.poly_name = 'line'
            self.n = taken('polys', self.poly_name)
            self.build_line()
            self.reset()
            return True
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

    def set_profile(self):
        inf = 0
        print('{}'.format(len(self.profile)))
        for i in range(1, len(self.profile)):
            if (self.profile[i] != self.profile[i-1]) or (i == len(self.profile) - 1):
                nprofile = self.profile[i-1]
                print('{} - {}'.format(i, nprofile))
                pname   = 'data/Profile{}.dat'.format(nprofile)
                ready   = pd.DataFrame({
                    'St.':self.stats.iloc[inf:i+1],
                    'x': self.x.iloc[inf:i+1],
                    'C': self.cond_ap.iloc[inf:i+1],
                    'R': self.rest_ap.iloc[inf:i+1],
                    'Ip':self.ip.iloc[inf:i+1],
                    'Op':self.op.iloc[inf:i+1]
                })
                if(os.path.exists(pname)):
                    prev_data = pd.read_csv(pname)
                    ready = pd.concat([prev_data, ready], axis=0)
                    ready.to_csv(pname, index=False)
                else:
                    ready.to_csv(pname, index=False)
                inf = i

    def reset(self):
        p = int(self.nplanilla)
        for profile in os.listdir('data/'):
            if 'Profile' in profile:
                self.profile    = 'data/{}'.format(profile)
                self.n          = int(profile[7])
                data            = pd.read_csv(self.profile)
                self.x          = data['x']
                self.cond_ap    = data['C']
                self.rest_ap    = data['R']
                self.ip         = data['Ip']
                self.op         = data['Op']
                self.stats      = data['St.']
                self.rest_ap.name   = 'RA'
                self.cond_ap.name   = 'CA'
                self.ip.name        = 'IP'
                self.op.name        = 'OP'
                self.build_line()
                self.lines_plot()
                add('polys', self.REPORT)

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
            'planilla':self.nplanilla,
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
            'planilla':self.nplanilla,
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
            'planilla':self.nplanilla,
            'n':self.n,
            'time':str(datetime.now()),
            'outputs': files,
        }
        self.filename = files

    def build_line(self):
        files = {
            'basic': 'scatt_{}_{}.png'.format(self.linetype, self.n),
            'lines': 'lines_{}_{}.png'.format(self.linetype, self.n),
        }
        poly = ''
        if self.linetype == 'R':
            poly = 'R'
        elif self.linetype == 'IO':
            poly = 'IO'
        elif self.linetype == 'C':
            poly = 'ivo'

        self.REPORT = {
            'poly':poly,
            'planilla':self.nplanilla,
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
            if int(self.nprofile) in self.firstday:
                if selflocs.iloc[idx-1] == None:
                    next_lon = abs(self.framed_locs.iloc[idx+1]['Lon'])
                    next_lat = abs(self.framed_locs.iloc[idx+1]['Lat'])
                    curr_lon = abs(row['Lon'])
                    curr_lat = abs(row['Lat'])
                    if next_lon < curr_lon:
                        new_lon = row['Lon'] + (math.copysign(1, row['Lon'])) * 0.00018
                    else:
                        new_lon = row['Lon'] - (math.copysign(1, row['Lon'])) * 0.00018

                    if next_lat < curr_lat:
                        new_lon = row['Lat'] + (math.copysign(1, row['Lat'])) * 0.00018
                    else:
                        new_lon = row['Lat'] - (math.copysign(1, row['Lat'])) * 0.00018
                else:
                    new_lat = (row['Lat'] + self.framed_locs.iloc[idx+1]['Lat']) / 2
                    new_lon = (row['Lon'] + self.framed_locs.iloc[idx+1]['Lon']) / 2

                self.framed_locs.iloc[idx]['Lat'] = new_lat
                self.framed_locs.iloc[idx]['Lon'] = new_lon

            elif int(self.nprofile) in self.secndday:
                if idx == (len(self.framed_locs) - 1):
                    prev_lon = abs(self.framed_locs.iloc[idx-1]['Lon'])
                    prev_lat = abs(self.framed_locs.iloc[idx-1]['Lat'])
                    curr_lon = abs(row['Lon'])
                    curr_lat = abs(row['Lat'])
                    if prev_lon < curr_lon:
                        new_lon = row['Lon'] + (math.copysign(1, row['Lon'])) * 0.00018
                    else:
                        new_lon = row['Lon'] - (math.copysign(1, row['Lon'])) * 0.00018

                    if prev_lat < curr_lat:
                        new_lon = row['Lat'] + (math.copysign(1, row['Lat'])) * 0.00018
                    else:
                        new_lon = row['Lat'] + (math.copysign(1, row['Lat'])) * 0.00018
                else:
                    print('{}/{}'.format(idx, len(self.framed_locs)))
                    new_lat = (row['Lat'] + self.framed_locs.iloc[idx+1]['Lat']) / 2
                    new_lon = (row['Lon'] + self.framed_locs.iloc[idx+1]['Lon']) / 2

                    #print('current:{} - next:{}'.format(row['Lat'], self.framed_locs.iloc[idx+1]['Lat']))
                    #print('\tnew lat: {}'.format(new_lat))

                self.framed_locs.iloc[idx]['Lat'] = new_lat
                self.framed_locs.iloc[idx]['Lon'] = new_lon
            else:
                print('not recognized profile')

    def add_locs(self):
        for i in range(1,5):
            pname   = 'data/Profile{}.dat'.format(i)
            self.nprofile = i
            data    = pd.read_csv(pname)
            nfirst  = data['St.'].iloc[0] - 1
            nlastt  = data['St.'].iloc[-1]
            locs    = pd.read_csv("data/locations.dat")

            self.framed_locs = locs.iloc[nfirst:nlastt]
            self.transf_locs()
            lat     = self.framed_locs['Lat'].reset_index()
            lon     = self.framed_locs['Lon'].reset_index()

            ready = pd.concat([self.stats, self.ip, self.op, self.rest_ap, lat['Lat'], lon['Lon']], axis=1)
            output_name = "data/Profile{}_with_locs".format(self.nprofile)
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
        filepath = 'prs\{}\outputs\{}'.format(self.pname, self.filename['basic'])
        plt.figure()
        plt.plot(self.x, self.ip, 'o', label='Data')
        plt.plot(self.x, self.op, 'o', label='Data')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def polys_plot(self):
        filepath = 'prs\{}\outputs\{}'.format(self.pname, self.filename['polys'])
        plt.figure()
        plt.plot(self.x_trained, self.output_ip, '-', label='Ip')
        plt.plot(self.x_trained, self.output_op, '-', label='Op')
        plt.ylim(-80, 80)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def lines_plot(self):
        filepath = 'prs\{}\outputs\{}'.format(self.pname, self.filename['lines'])
        #plt.figure()
        fig, ax = plt.subplots()

        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        if self.linetype == 'IO':
            plt.ylim(-80, 80)
            ax.grid()
            ax.plot(self.x, self.ip, '-', label='Ip', color='red')
            ax.plot(self.x, self.ip, 'o', color='red')
            ax.plot(self.x, self.op, '-', label='Op', color='blue')
            ax.plot(self.x, self.op, 'o', color='blue')
            ax.set_ylabel('C')
        elif self.linetype == 'R':
            ax.set_yscale('log')
            ax.plot(self.x, self.rest_ap, '-', label='Ra', color='black')
            ax.plot(self.x, self.rest_ap, 'o', color='black')
            ax.set_ylabel('R')
        elif self.linetype == 'C':
            ax.set_yscale('log')
            ax.plot(self.x, self.cond_ap, '-', label='Ca', color='black')
            ax.plot(self.x, self.cond_ap, 'o', color='black')
            ax.set_ylabel('C')
        else:
            print('unrecognized option')

        ax.set_title('Perfil {}'.format(self.n))
        ax.set_xlabel('x(m)')

        ax_top = ax.twiny()
        ax_top.set_xlim(ax.get_xlim())
        ax_top.set_xticks(self.x)
        ax_top.set_xticklabels(self.stats)
        ax_top.set_xlabel("Stations")

        ax.legend()
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def complete_plot_ipop(self):
        filepath = 'prs\{}\outputs\{}'.format(self.pname, self.filename['complete'])
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
        filepath = 'prs\{}\outputs\{}'.format(self.pname, self.filename['complete'])
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

    def boxplots(self, which):
        filepath = 'prs\{}\outputs\{}'.format(self.pname, 'boxplot_p{}_{}'.format(self.nprofile, self.n))
        ready = pd.DataFrame()
        if self.linetype == 'R':
            for i in range(1, 10):
                df = pd.read_csv('data\Profile{}.dat'.format(i))
                ready = pd.concat([ready, df['R']], axis=1)
        elif self.linetype == 'C':
            for i in range(1, 10):
                df = pd.read_csv('data\Profile{}.dat'.format(i))
                ready = pd.concat([ready, df['C']], axis=1)
        else:
            df = pd.read_csv('data\Profile{}.dat'.format(int(which)))

        ready.plot(kind='box', title='Aparente Resistivity(ohm)')
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

    def heatmap(self):
        df      = pd.read_csv('data/Grid')
        lats    = df['Lat'].to_numpy()
        lons    = df['Lon'].to_numpy()
        z       = None
        newz    = None
        norm    = None
        title   = None
        bw_method = 0.4
        if self.linetype == 'R':
            z   = df['RA'].to_numpy()
            title = 'Resistivity (ohm)'
        elif self.linetype == 'C':
            z   = df['CA'].to_numpy()
            title = 'Conductivity'
        elif self.linetype == 'I':
            z   = df['IP'].to_numpy()
            title = 'IP-conductivity'
        elif self.linetype == 'O':
            z   = df['OP'].to_numpy()
            title = 'OP-conductivity'

        filepath = 'heat_map_talacasto_{}.png'.format(self.linetype)

        coords  = np.vstack([lons, lats])
        if (self.linetype == 'I' or self.linetype == 'O'):
            newz = z + abs(z.min())
            bw_method = 0.3

        kde1    = gaussian_kde(
            coords,
            weights=newz,
            bw_method=bw_method
        )
        points  = np.column_stack([lons, lats])
        hull    = ConvexHull(points)
        #hull    = Delaunay(points)

        xmin, ymin = points[hull.vertices].min(axis=0)
        xmax, ymax = points[hull.vertices].max(axis=0)

        xi = np.linspace(xmin, xmax, 300)
        yi = np.linspace(ymin, ymax, 300)
        xi, yi = np.meshgrid(xi, yi)
        zi = kde1(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

        hull_p  = Path(points[hull.vertices])
        mask    = hull_p.contains_points(np.column_stack([xi.ravel(), yi.ravel()])).reshape(xi.shape)
        zi[~mask] = np.nan

        fig, ax = plt.subplots(figsize=(8,6))
        if (self.linetype == 'R'):
            norm= LogNorm(vmin=np.nanmin(zi),
                          vmax=np.nanmax(zi))

        im  = ax.pcolormesh(
            xi, yi, zi,
            cmap="jet",
            shading="auto",
            norm=norm
        )
        ax.scatter(lons, lats, c="cyan", s=10, edgecolor="k")
        #cmap = plt.contourf(xi, yi, zi)
        ax.set_xlim(-68.752,-68.736)
        ax.set_ylim(-31.028,-31.017)
        ax.set_xlabel("Lon")
        ax.set_ylabel("Lat")
        ax.set_title(title)

        plt.colorbar(im, label=title)
        #fig.colorbar(cmap)
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

