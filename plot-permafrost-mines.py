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

CS1 = m.contour(x,y,permaforst_extent,clevs,linewidths=0.5,colors='k',animated=True)
CS2 = m.contourf(x,y,permaforst_extent,clevs,cmap=cm,animated=True)

# draw coastlines, parallels, meridians.\n",
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawstates(linewidth=0.5)

parallels = np.arange(0.,81,10.)

#reading the communities file
#north_communities2.csv
df = pd.read_csv('Mine_Site_Locations2.csv')
#df = pd.read_csv('communities.csv', header=None, names=['name', 'lat', 'lon', 'pop', 'type', 'province'])

names = ['Québec', 'Northwest Territories', 'Nunavut', 'Yukon', 'Newfoundland and Labrador']

for lat, lon in zip(df.Latitude, df.Longitude):
    x, y = m(lon, lat)
    m.scatter(x, y, s=60, c='red', edgecolor='black')



#plt.legend()


#plt.title('Figure 3: Grid telescoping into Nunavut\nfor convection permitting simulations', y=-0.12, fontsize=40)
plt.savefig('permafrost_communities_mines.png', pad_inches=0.0, bbox_inches='tight', transparent=True)
