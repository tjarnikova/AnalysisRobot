#runs directory for the model output, must be changed if different
baseDir = '/gpfs/afm/greenocean/software/runs/'

import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import glob
import warnings
import sys
warnings.filterwarnings('ignore')
import argparse
from argparse import RawTextHelpFormatter

## code to parse command line input and provide a help description
parser = argparse.ArgumentParser(description=  """   
    script for simple (non-projected) visualization of a single variable in a single file of raw output from PLANKTOM
    user sets model run, filetype, variable, year, month, depth index, y extent, and x extent
    
    Important: assumes output is in /gpfs/afm/greenocean/software/runs/
    (Else baseDir variable on line 2 of this script must be changed)
    
    command-line usage:
    python simple_map.py model_run_name filetype variable year month depth_index y_start_index y_end_index x_start_index x_end_index
    
    example (which produces full map, january):
    python simple_map.py TOM12_TJ1AS1 ptrc_T DIC 1950 0 0 0 149 0 182 
    note that it's python indexing, ie january is 0, first x coordinate / depth coordinate is 0, etc

    (will fail if you try to give it years/filetypes/variables that the model output doesn't have)
    
    > produces .jpg in directory where it is run
    > requires standard modules (incl python and netCDF4) to be loaded (typically using modadd)
    
    Other notes:
    > if visualizing 3-D field instead of 4-D field (eg Cflx instead of DIC), still put '0' for depth index
    > tries to optimize colorbars based on projected values. for Cflx, centers on 0 and uses divergent colourmap
    written by TJSJ 2022 (T.Jarnikova@uea.ac.uk) 
    """, formatter_class=RawTextHelpFormatter)

parser.add_argument('modnam', default='test_model', help='model name')
parser.add_argument('filetype', default='grid_T', help='filetype, eg: grid_T, grid_T, ptrc_T, icemod, grid_V')
parser.add_argument('varname', default='DIC', help='var name, must be in filetype chosen (eg DIC in ptrc_T)')
parser.add_argument('year', default=9999, help='year to analyze')
parser.add_argument('month', default='0', help='month')
parser.add_argument('depthind', default=0, help='depth index to plot for (eg 0 is surface, if chosen variable is 3D instead of 4D (eg Cflx), must choose 0)')
parser.add_argument('ystart', default=9999, help='y index at which to start plotting')
parser.add_argument('yend', default='grid_T', help='y index at which to end plotting')
parser.add_argument('xstart', default=9999, help='x index at which to start plotting')
parser.add_argument('xend', default=999, help='x index at which to end plotting')



#read in variables and convert as necessary to int
args=parser.parse_args()
modname = args.modnam
year = int(args.year)
ncstr = (args.filetype)
var = (args.varname)
month = int(args.month)
ystart = int(args.ystart)
yend = int(args.yend)
xstart = int(args.xstart)
xend = int(args.xend)
depthind = int(args.depthind)

print(f'Plotting for run {modname}, years {year}')
print(f'variable {var} (in filepattern {ncstr}), month {month} (january = 0)')
print(f'y start index {ystart}, y end index {yend}, x start index {xstart}, x end index {xend}')
print(f'depth level {depthind}')

#we assume that model output is in this directory tree, change if nec. 
#access first file in timeseries, get out units and longname 


### access depth 
tnc = nc.Dataset('/gpfs/data/greenocean/software/resources/regrid/mesh_mask3_6.nc')
tdepths = (tnc['gdept_1d'][0,:])
t_depth = tdepths[depthind]
tland = (tnc['tmask'][0,0,:,:])
tland = tland.astype(float)
tland[tland==1]=3
tland[tland==0]=1
tland[tland==3]=np.nan

w = glob.glob(f'{baseDir}{modname}/*{year}*{ncstr}.nc')
ncnam = (w[0])
tnc = nc.Dataset(ncnam)
longname = tnc[var].long_name
units = tnc[var].units
tnc = nc.Dataset(ncnam)
tvar0 = tnc[var][:]
if (tvar0.ndim == 4):
    tvar = tvar0[month,depthind,ystart:yend,xstart:xend]
else:
    tvar = tvar0[month,ystart:yend,xstart:xend]
tvar[tvar == 0] = np.nan
## set plot maxs and plot minx
tcmap = 'viridis'
plt_min = 0.8*np.nanmean(tvar)
plt_max = 1.2*np.nanmean(tvar)

if var == 'Cflx':
    tcmap = 'RdBu'
    flxout = (np.nanmax(tvar))
    flxin = (np.abs(np.nanmin(tvar)))
    cbarmax = (np.max([flxout,flxin]))
    plt_min = -0.75*cbarmax
    plt_max = 0.75*cbarmax

    
fact = 0.4
fig, axs = plt.subplots(1,1, figsize=(20*fact, 15*fact), facecolor='w', edgecolor='k')
pltmesh = axs.pcolormesh(tvar, cmap = tcmap, vmin = plt_min, vmax = plt_max)
pltmesh2 = axs.pcolormesh(tland, cmap = 'Greys', vmin = 0, vmax = 1.2)
fig.colorbar(pltmesh, ax=axs, orientation = 'horizontal', label = units)
axs.set_yticks([]); axs.set_xticks([]);
mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.suptitle(f'{modname} {var} ({longname})\n year {year}, month {mons[month]}, depth level {depthind} ({int(t_depth)}m)')
fig.savefig(f'SimpleMap_{modname}_{var}_{mons[month]}{year}_y{ystart}-{yend}_x{xstart}-{xend}_level{depthind}.jpg')