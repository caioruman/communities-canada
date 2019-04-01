from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pandas as pd

#from rpn.rpn import RPN
#from rpn.domains.rotated_lat_lon import RotatedLatLon
#from rpn import level_kinds

'''

Reads a RPN file and plot the domain over the globe

'''

#r = RPN('/glacier/caioruman/Data/Geophys/PanArctic0.5/pan_artic_me_0.5')
#graham
#r = RPN('/home/cruman/scratch/CanArc_004deg_1500x900.fst')
#cedar
nc = Dataset('CanArc_004deg_1500x900.nc')

lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]
#var = "MSKC"

#me = r.variables[var][0,0]

#lon, lat = r.get_longitudes_and_latitudes_for_the_last_read_rec()

m = Basemap(resolution='i',projection='ortho',lon_0=-105,lat_0=70)
#m = Basemap(resolution='l', projection='', 

#fig1 = plt.figure(figsize=(7, 11), frameon=False, dpi=100)
fig1 = plt.figure(figsize=(14, 22), frameon=False, dpi=150)
ax = fig1.add_axes([0.1,0.1,0.8,0.8])

print(lon[:,0].shape)
print(lat[0,:].shape)
print(lon.shape)
print(lat.shape)
#newlon = np.where(lon <= 180, lon, lon - 360)

#for i in range(0,lat[0,:].shape[0],5):
#    print(lon[:,i])
#    print(lat[:,i])
#    x, y = m(newlon[:,i], lat[:,i])
#     x = newlon[:,i]
#     y = lat[:,i]
#    print(x)
#    print(y)
#     m.plot(x, y, color='red', linewidth=0.25)

#for i in range(0,lon[:,0].shape[0],5):
#    x, y = m(newlon[i,:], lat[i,:])
#    m.plot(x, y, color='red', linewidth=0.25)

ii = [0,-1]

for i in ii:
        
    x,y = m(lon[:,i],lat[:,i])
    m.plot(x,y,color='black', linewidth=3)

    x,y = m(lon[i,:],lat[i,:])
    m.plot(x,y,color='black', linewidth=3)

# Blending domain
bb = 40
ii = [bb,-bb]

#for i in ii:

#    x,y = m(lon[bb:-bb,i],lat[bb:-bb,i])
#    m.plot(x,y,color='red')

#    x,y = m(lon[i,bb:-bb],lat[i,bb:-bb])
#    m.plot(x,y,color='red')

nc.close()


m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawstates(linewidth=0.5)



#reading the communities file
#north_communities2.csv
df = pd.read_csv('north_communities2.csv', header=None, names=['name', 'lat', 'lon', 'pop', 'type', 'province'])
colors = ['red', 'dodgerblue', 'darkgreen', 'yellow', 'darkorange']

counts = []
# Yukon = 1; NWT = 2; Nu = 3, Quebec = 4, NF = 5
order = [4, 2, 3, 1, 5]
names = ['Quebec', 'Northwest Territories', 'Nunavut', 'Yukon', 'Newfoundland and Labrador']

for (item,color) in zip(df['province'].unique(), colors):
    
    if item == 'Quebec':
        ll = 50
    else:
        ll = 50
    print(item)
    temp = df.loc[(df['province'] == item) & (df['lat'] > ll)]
    counts.append(temp.name.count())
    for lat, lon in zip(temp.lat, temp.lon):
        # Plot the points
     #   print(lat, lon)
        x, y = m(lon, lat)
        m.scatter(x, y, s=60, c=color, edgecolor='black')

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

#m.drawcoastlines(linewidth=0.5)
#m.drawcountries(linewidth=0.5)
#m.drawstates(linewidth=0.5)
#m.drawlsmask()
m.shadedrelief()

#reading the communities file
#north_communities2.csv



#plt.title('Figure 3: Grid telescoping into Nunavut\nfor convection permitting simulations', y=-0.12, fontsize=40)
plt.savefig('domain_nogrid_color.png', pad_inches=0.0, bbox_inches='tight', transparent=True)
