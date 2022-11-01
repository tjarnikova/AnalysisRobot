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
    script for summarizing mean model quantities over a set of years
    
    command-line usage:
    python summary_maps.py modnam yearstart yearend filetype varname depthindex
    example:
    python summary_maps.py TOM12_TJ_1AS1 1950 1960 diad_T Cflx 0
    
    Important: 
    -> assumes output is in /gpfs/afm/greenocean/software/runs/
        (Else baseDir variable on line 2 must be changed)
    -> requires modadd (adding standard modules, esp. python and netCDF4)
    
    Other info:
    -> produces .jpg in directory where it is run
    -> Data visualized in six subplots as follows:
        -first row global ocean:
            full year mean for years selected, 
            austral summer (months 12-2) mean for years selected, 
            austral winter (months 6-8) mean for years selected
        -second row SO south of - 30 (same 3 subplots as above)


    Other notes:
    -> if want averages for only one year, simply put same year twice (eg: TOM12_RW_M13V 1970 1970 ptrc_T DIC 0)
    -> if visualizing 3-D field instead of 4-D field (eg Cflx instead of DIC), still put '0' for depth index
    -> tries to optimize colorbars based on projected values. for Cflx, centers on 0 and uses divergent colourmap
    written by TJSJ 2022 (T.Jarnikova@uea.ac.uk) 
    """, formatter_class=RawTextHelpFormatter)

parser.add_argument('modnam', default='test_model', help='model name')
parser.add_argument('yearstart', default=9999, help='first year to analyze')
parser.add_argument('yearend', default=9999, help='last year to analyze')
parser.add_argument('filetype', default='grid_T', help='filetype, eg: grid_T, grid_T, ptrc_T, icemod, grid_V')
parser.add_argument('varname', default='DIC', help='var name, must be in filetype chosen (eg DIC in ptrc_T)')
parser.add_argument('depthind', default=0, help='depth index to plot for (eg 0 is surface, if chosen variable is 3D instead of 4D (eg Cflx), must choose 0)')


#read in variables and convert as necessary to int
args=parser.parse_args()
modname = args.modnam
yearstart = int(args.yearstart)
yearend = int(args.yearend)
ncstr = args.filetype
var = args.varname
depthind = int(args.depthind)

print(f'Plotting for run {modname}, years {yearstart}-{yearend}')
print(f'variable {var} (in filepattern {ncstr})')
print(f'depth level {depthind}')

#we assume that model output is in this directory tree, change if nec. 
#access first file in timeseries, get out units and longname 
w = glob.glob(f'{baseDir}{modname}/*{yearstart}*{ncstr}.nc')
ncnam = (w[0])
tnc = nc.Dataset(ncnam)
longname = tnc[var].long_name
units = tnc[var].units

### access depth 
tnc = nc.Dataset('/gpfs/data/greenocean/software/resources/regrid/mesh_mask3_6.nc')
tdepths = (tnc['gdept_1d'][0,:])
t_depth = tdepths[depthind]
tland = (tnc['tmask'][0,0,:,:])
tland = tland.astype(float)
tland[tland==1]=3
tland[tland==0]=1
tland[tland==3]=np.nan

#prepare array of years to loop through, and storage arrays for output
# and for max and min for plotting
yrs = np.arange(yearstart,yearend+1,1)
noyrs = len(yrs)

summer_stor = np.zeros([noyrs,149,182])
winter_stor = np.zeros([noyrs,149,182])
allyear_stor = np.zeros([noyrs,149,182])

plt_min = 0; plt_max = 0

for y in range(0,noyrs):
    
    ts_index = 0
    yr = yrs[y]
    #find relevant nc using wildcards and the glob package
    w = glob.glob(f'{baseDir}{modname}/*{yr}*{ncstr}*.nc')
    ncnam = (w[0])
    
    #open dataset and extract relevant variable 
    tnc = nc.Dataset(ncnam)
    tvar0 = tnc[var][:]
    ## if array is 4 dimensional (Time, depth, y, x), slice to get relevant depth
    #else it should be 3dimensional and you just take whole array
    if (tvar0.ndim == 4):
        tvar = tvar0[:,depthind,:,:]
    else:
        tvar = tvar0[:]
    #set up some rough mins, maxs for for colourbar  
    tvar[tvar == 0] = np.nan
    #get out summer, ie months december, jan, feb, and average accross months
    this_summer = np.zeros([3,149,182])
    this_summer[0,:,:] = tvar[11,:,:]
    this_summer[1:3,:,:] = tvar[0:2,:,:]
    ## average accross the 3 months and put into storage array
    summer_stor[y,:,:] = np.nanmean(this_summer,axis = 0)
    #winter is months 6-8, so python indices 5-8 (8 isn't counted in python indexing here)
    winter_stor[y,:,:] = np.nanmean(tvar[5:8,:,:],axis = 0)
    allyear_stor[y,:,:] = np.nanmean(tvar[:,:,:],axis = 0)
    
## average out the stored arrays
## average out the stored arrays
winter_stor_mn = np.nanmean(winter_stor,axis =0)
summer_stor_mn = np.nanmean(summer_stor,axis =0)
allyear_stor_mn = np.nanmean(allyear_stor,axis =0)

# get only the SO
winter_stor_mn_SO = winter_stor_mn[0:50,:]
summer_stor_mn_SO = summer_stor_mn[0:50,:]
allyear_stor_mn_SO = allyear_stor_mn[0:50,:]

## set plot maxs and plot minx
tcmap = 'viridis'
plt_min = 0.8*np.nanmean(allyear_stor_mn)
plt_max = 1.2*np.nanmean(allyear_stor_mn)
plt_min_SO = 0.9*np.nanmean(allyear_stor_mn_SO)
plt_max_SO = 1.1*np.nanmean(allyear_stor_mn_SO)

if var == 'Cflx':
    tcmap = 'RdBu'
    flxout = (np.nanmax(allyear_stor_mn))
    flxin = (np.abs(np.nanmin(allyear_stor_mn)))
    cbarmax = (np.max([flxout,flxin]))
    plt_min = -0.75*cbarmax
    plt_max = 0.75*cbarmax
    flxout_SO = (np.nanmax(allyear_stor_mn_SO))
    flxin_SO = (np.abs(np.nanmin(allyear_stor_mn_SO)))
    cbarmax_SO = (np.max([flxout_SO,flxin_SO]))
    plt_min_SO = -0.75*cbarmax_SO
    plt_max_SO = 0.75*cbarmax_SO    
    
    
to_plt = [allyear_stor_mn, summer_stor_mn, winter_stor_mn,\
         allyear_stor_mn_SO, summer_stor_mn_SO, winter_stor_mn_SO]
seas = ['full year', 'austral summer (months 12-2)', 'austral winter (months 6-8)',\
       'full year', 'austral summer (months 12-2)', 'austral winter (months 6-8)',]
fact = 0.7
fig, axs = plt.subplots(2,3, figsize=(20*fact, 14*fact), facecolor='w', edgecolor='k')
axs = axs.ravel()
for i in range(0,3):
    pltmesh = axs[i].pcolormesh(to_plt[i], cmap = tcmap, vmin = plt_min, vmax = plt_max)
    pltmesh2 = axs[i].pcolormesh(tland, cmap = 'Greys', vmin = 0, vmax = 1.2)
    fig.colorbar(pltmesh, ax=axs[i], orientation = 'horizontal', label = units)
    axs[i].set_yticks([]); axs[i].set_xticks([]);
    axs[i].set_title(f'{seas[i]}\n Global')
    
for i in range(3,6):
    pltmesh = axs[i].pcolormesh(to_plt[i], cmap = tcmap, vmin = plt_min_SO, vmax = plt_max_SO)
    pltmesh2 = axs[i].pcolormesh(tland[0:50,:], cmap = 'Greys', vmin = 0, vmax = 1.2)
    fig.colorbar(pltmesh, ax=axs[i], orientation = 'horizontal', label = units)
    axs[i].set_yticks([]); axs[i].set_xticks([]);
    axs[i].set_title(f'{seas[i]}\n Southern Ocean (south of -30$^\circ$S)')

plt.suptitle(f'Mean {modname} {var} ({longname})\n years {yearstart}-{yearend}, depth level {depthind} ({int(t_depth)}m)')
fig.savefig(f'SummaryPlot_{modname}_{var}_{yearstart}-{yearend}_level_{depthind}.jpg')