from mpl_toolkits.basemap import Basemap, maskoceans
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pandas as pd
import matplotlib as mpl

'''

Reads a RPN file and plot the domain over the globe

'''

#r = RPN('/glacier/caioruman/Data/Geophys/PanArctic0.5/pan_artic_me_0.5')
#graham
#r = RPN('/home/cruman/scratch/CanArc_004deg_1500x900.fst')
#cedar
nc = Dataset('teufel_permaice.nc')

lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]

permafrost_type = nc.variables['num_code'][:].squeeze()
permaforst_extent = nc.variables['extent'][:].squeeze()

lons, lats = np.meshgrid(lon,lat)
permaforst_extent = permaforst_extent.astype(float)
permaforst_extent2 = permaforst_extent.copy()
permaforst_extent2[permaforst_extent==0] = -1
permaforst_extent[permaforst_extent==0] = np.nan


colors = ["#bdd7e7", "#6baed6", "#3182bd", "#08519c"]
cm = mpl.colors.ListedColormap(colors[::-1])
cm.set_bad(color='#dddddd')
m = Basemap(resolution='l',projection='npstere',boundinglat=45,lon_0=270,round=True)

fig1 = plt.figure(figsize=(14, 22), frameon=False, dpi=150)
ax = fig1.add_axes([0.1,0.1,0.8,0.8])
# set desired contour levels.\n",
clevs = np.arange(0,5,1)
clevs2 = np.arange(-1,5,1)
# compute native x,y coordinates of grid.\n",
x, y = m(lons, lats)
# define parallels and meridians to draw.\n",
parallels = np.arange(-80.,90,20.)
meridians = np.arange(0.,360.,20.)

newdata2 = maskoceans(lons, lats, permaforst_extent, resolution = 'h', grid = 1.25, inlands=False)

m.drawlsmask(land_color='white',ocean_color='#dddddd')

CS1 = m.contour(x,y,permaforst_extent,clevs,linewidths=0.5,colors='k',animated=True, zorder = 2)
CS2 = m.contourf(x,y,permaforst_extent,clevs,cmap=cm,animated=True, zorder = 1)

# draw coastlines, parallels, meridians.\n",
m.drawcoastlines(linewidth=0.5, zorder = 1)
m.drawcountries(linewidth=0.5, zorder = 1)
m.drawstates(linewidth=0.5, zorder = 1)

parallels = np.arange(0.,81,10.)

#reading the communities file
#north_communities2.csv
df = pd.read_csv('communities.csv', encoding="ISO-8859-1", index_col=0)
df = df.sort_values(by=['Province'])
#df = pd.read_csv('communities.csv', header=None, names=['name', 'lat', 'lon', 'pop', 'type', 'province'])
colors = ['green', 'indigo', 'red', 'yellow', 'darkorange']

counts = []
# Yukon = 1; NWT = 2; Nu = 3, Quebec = 4, NF = 5
order = [4, 2, 3, 1, 5]
names = ['Québec', 'Northwest Territories', 'Nunavut', 'Yukon', 'Newfoundland and Labrador']

for prov, color in zip(names, colors):
    temp = df.loc[df['Province'] == prov]

    cc = 0
    for lat, lon in zip(temp.Lat, temp.Lon):
        if (prov == "Québec") and lat < 50:
            continue
        else:
            cc += 1
        x, y = m(lon, lat)
        m.scatter(x, y, s=60, c=color, edgecolor='black', zorder = 3)
    if (prov == "Québec"):
        counts.append(cc)
    else:
        counts.append(temp.Lat.count())

c = []
for a, b, e, f in zip(counts, order, names, colors):
    c.append((a,b,e,f))

from operator import itemgetter

d = sorted(c,key=itemgetter(1))

line1 = plt.Line2D(range(10), range(10), marker='s', color=d[0][3])
line2 = plt.Line2D(range(10), range(10), marker='s',color=d[1][3])
line3 = plt.Line2D(range(10), range(10), marker='s',color=d[2][3])
line4 = plt.Line2D(range(10), range(10), marker='s',color=d[3][3])
line5 = plt.Line2D(range(10), range(10), marker='s', color=d[4][3])
plt.legend((line1,line2,line3, line4, line5),
           ('{0}: {1}'.format(d[0][2], d[0][0]), '{0}: {1}'.format(d[1][2], d[1][0]),
            '{0}: {1}'.format(d[2][2], d[2][0]), '{0}: {1}'.format(d[3][2], d[3][0]),
            '{0}: {1}'.format(d[4][2], d[4][0])),numpoints=8, loc=3,
          bbox_to_anchor=(0., 1.02, 1., .102),ncol=2,mode="expand", borderaxespad=0,fontsize=20, fancybox=True, framealpha=0.1)

#plt.legend()


#plt.title('Figure 3: Grid telescoping into Nunavut\nfor convection permitting simulations', y=-0.12, fontsize=40)
plt.savefig('permafrost_communities_v3.png', pad_inches=0.0, bbox_inches='tight', transparent=True)
