import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys
import warnings
warnings.filterwarnings('ignore')
import cmocean as cm
from importlib import reload
import glob
import os
import pandas as pd
import cflx as cflx

plt.rcParams.update({'font.size': 10})
font = {'family' : 'normal',
'weight' : 'normal',
'size'   : 10}

plt.rc('font', **font)
def make_summaryplot(tr, resdir, syear, eyear):

    tempmin = 2; tempmax = 30
    salmin = 33; salmax = 36
    chlmin = 0; chlmax = 2


    tmin, tmax = cflx.max_min_yrs(tr, resdir)

    if (tmin <1998) & (tmax > 2010):
        yrst = 1998
        yrend = 2010
    else:
        yrst = syear
        yrend = eyear

    tlist = cflx.make_yearlist(yrst, yrend, 'grid_T', tr, resdir)
    noyrs = yrend - yrst

    w = xr.open_mfdataset(tlist)
    yrly_temp_surf = np.zeros([noyrs,12,149,182])
    yrly_sal_surf = np.zeros([noyrs,12,149,182])
    for i in range(0,noyrs):
        ind = i*12
        yrly_temp_surf[i,:,:,:] = w['votemper'][ind:ind+12,0,:,:]
        yrly_sal_surf[i,:,:,:] = w['vosaline'][ind:ind+12,0,:,:]
    yrly_temp_surf = np.nanmean(yrly_temp_surf, axis = 0)
    yrly_sal_surf = np.nanmean(yrly_sal_surf, axis = 0)

    tlist = cflx.make_yearlist(yrst, yrend, 'diad_T', tr, resdir)
    w = xr.open_mfdataset(tlist)
    yrly_chl_surf = np.zeros([noyrs,12,149,182])
    for i in range(0,noyrs):
        ind = i*12
        yrly_chl_surf[i,:,:,:] = w['TChl'][ind:ind+12,0,:,:]
    yrly_chl_surf = np.nanmean(yrly_chl_surf, axis = 0)

    summer_temp_surf = (yrly_temp_surf[0,:,:]*31+yrly_temp_surf[1,:,:]*28+yrly_temp_surf[11,:,:]*31)/90
    winter_temp_surf = (yrly_temp_surf[5,:,:]*30+yrly_temp_surf[6,:,:]*31+yrly_temp_surf[7,:,:]*31)/92
    summer_sal_surf = (yrly_sal_surf[0,:,:]*31+yrly_sal_surf[1,:,:]*28+yrly_sal_surf[11,:,:]*31)/90
    winter_sal_surf = (yrly_sal_surf[5,:,:]*30+yrly_sal_surf[6,:,:]*31+yrly_sal_surf[7,:,:]*31)/92
    summer_chl_surf = (yrly_chl_surf[0,:,:]*31+yrly_chl_surf[1,:,:]*28+yrly_chl_surf[11,:,:]*31)/90 * 1e6
    winter_chl_surf = (yrly_chl_surf[5,:,:]*30+yrly_chl_surf[6,:,:]*31+yrly_chl_surf[7,:,:]*31)/92 * 1e6
     
    
    yrly_temp_surf = np.nanmean(yrly_temp_surf, axis = 0)
    yrly_sal_surf = np.nanmean(yrly_sal_surf, axis = 0)
    yrly_chl_surf = np.nanmean(yrly_chl_surf, axis = 0) * 1e6
    
    summer_temp_surf[summer_temp_surf ==0] = np.nan
    winter_temp_surf[winter_temp_surf ==0] = np.nan
    yrly_temp_surf[yrly_temp_surf ==0] = np.nan
    summer_sal_surf[summer_sal_surf ==0] = np.nan
    winter_sal_surf[winter_sal_surf ==0] = np.nan
    yrly_sal_surf[yrly_sal_surf ==0] = np.nan
    summer_chl_surf[summer_chl_surf ==0] = np.nan
    winter_chl_surf[winter_chl_surf ==0] = np.nan
    yrly_chl_surf[yrly_chl_surf ==0] = np.nan   
    
    fact = 0.65
    fig, axs = plt.subplots(3,3, figsize=(20*fact, 18*fact), facecolor='w', edgecolor='k')
    axs = axs.ravel()
    ind = 0
    w = axs[0+ind].pcolormesh(summer_temp_surf, cmap = cm.cm.thermal, vmin = tempmin, vmax = tempmax)
    fig.colorbar(w, ax=axs[0+ind], orientation = 'horizontal', label = 'degC', aspect = 50)
    axs[0+ind].set_title('Dec-Feb surface temp')
    w = axs[1+ind].pcolormesh(winter_temp_surf, cmap = cm.cm.thermal, vmin = tempmin, vmax = tempmax)
    fig.colorbar(w, ax=axs[1+ind], orientation = 'horizontal', label = 'degC', aspect = 50)
    axs[1+ind].set_title('Jun-Aug surface temp')
    w = axs[2+ind].pcolormesh(yrly_temp_surf, cmap = cm.cm.thermal, vmin = tempmin, vmax = tempmax)
    fig.colorbar(w, ax=axs[2+ind], orientation = 'horizontal', label = 'degC', aspect = 50)
    axs[2+ind].set_title('yrly surface temp')
    
    ###
    ind = 3
    w = axs[0+ind].pcolormesh(summer_sal_surf, cmap = cm.cm.haline, vmin = salmin, vmax = salmax)
    fig.colorbar(w, ax=axs[0+ind], orientation = 'horizontal', label = 'g/kg', aspect = 50)
    axs[0+ind].set_title('Dec-Feb surface sal')
    w = axs[1+ind].pcolormesh(winter_sal_surf, cmap = cm.cm.haline, vmin = salmin, vmax = salmax)
    fig.colorbar(w, ax=axs[1+ind], orientation = 'horizontal', label = 'g/kg', aspect = 50)
    axs[1+ind].set_title('Jun-Aug surface sal')
    w = axs[2+ind].pcolormesh(yrly_sal_surf, cmap = cm.cm.haline, vmin = salmin, vmax = salmax)
    fig.colorbar(w, ax=axs[2+ind], orientation = 'horizontal', label = 'g/kg', aspect = 50)
    axs[2+ind].set_title('yrly surface sal')

    ind = 6
    w = axs[0+ind].pcolormesh(summer_chl_surf, cmap = cm.cm.algae, vmin = chlmin, vmax = chlmax)
    fig.colorbar(w, ax=axs[0+ind], orientation = 'horizontal', label = 'µg/L', aspect = 50)
    axs[0+ind].set_title('Dec-Feb surface chl')
    w = axs[1+ind].pcolormesh(winter_chl_surf, cmap = cm.cm.algae, vmin = chlmin, vmax = chlmax)
    fig.colorbar(w, ax=axs[1+ind], orientation = 'horizontal', label = 'µg/L', aspect = 50)
    axs[1+ind].set_title('Jun-Aug surface chl')
    w = axs[2+ind].pcolormesh(yrly_chl_surf, cmap = cm.cm.algae, vmin = chlmin, vmax = chlmax)
    fig.colorbar(w, ax=axs[2+ind], orientation = 'horizontal', label = 'µg/L', aspect = 50)
    axs[2+ind].set_title('yrly surface chl')
    
    for i in range(0,9):
        axs[i].set_xticklabels([])
        axs[i].set_yticklabels([])
    plt.suptitle(f'{tr} T, S, Chl surface overview, years {yrst}-{yrend}', fontsize = 15, y = 0.92)
    
    tfil = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{tr}/A01_SurfaceSummary.jpg'
    print(tfil)
    fig.savefig(tfil)
    
try:
    make_summaryplot(tr, resdir)
except:
    pass