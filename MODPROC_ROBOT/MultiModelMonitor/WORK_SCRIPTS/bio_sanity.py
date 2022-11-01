#bio_sanity

import matplotlib.pyplot as plt
import glob
import xarray as xr
import sys
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/MO_pipeline/')
import scendict as sc
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/MODPROC_ROBOT/MultiModelMonitor/WORK_SCRIPTS')
import breakdown as bp
import numpy as np


def get_sanity(tr, baseDir, startyear = -99,\
               sdir = '/gpfs/home/mep22dku/scratch/SOZONE/MODPROC_ROBOT/MultiModelMonitor/OUTPUT/'):
    
    fact = 0.5
    fig, axs = plt.subplots(3,2, figsize=(20*fact, 14*fact), facecolor='w', edgecolor='k')
    axs = axs.ravel()

    #case where we want to get rid of spinup years
    if startyear < 0:
        tmin, tmax = bp.max_min_yrs(tr, baseDir)
    if startyear > 0:
        tmin, tmax = bp.max_min_yrs(tr, baseDir)
        tmin = startyear
    print(f'making sanity for run {tr}: {tmin}-{tmax}')
    
    t_yearlist = bp.make_yearlist(tmin,tmax,'ptrc',tr, baseDir)
    tds_ptrc = xr.open_mfdataset(t_yearlist, chunks={'time_counter': 120})
    t_yearlist = bp.make_yearlist(tmin,tmax,'diad',tr, baseDir)
    tds_diad = xr.open_mfdataset(t_yearlist, chunks={'time_counter': 120})
    
    t_dsets = [tds_ptrc, tds_ptrc, tds_diad, tds_diad, tds_diad]
    t_vars = ['GOC', 'POC', 'EXP', 'PPT', 'TChl']
    
    td = tds_ptrc.indexes['time_counter'].to_datetimeindex()
    
    for x in range(0,5):
        tds = t_dsets[x]; tvar = t_vars[x]
        print(tvar)
        yrs = tds[tvar].shape[0]/12

        gocmean = np.zeros(int(yrs)*12)
        gocmax = np.zeros(int(yrs)*12)
        ind = 0
        for i in range(0,int(yrs)):
            if i%30 == 0:
                print(i)
            goc = tds[tvar][ind:ind+12,:,:,:].values
            goc[goc == 0] = np.nan
            w = np.nanmean(np.nanmean(np.nanmean(goc, axis = 3), axis =2), axis =1)
            gocmean[ind:ind+12] = (w)
            w = np.nanmax(np.nanmax(np.nanmax(goc, axis = 3), axis =2), axis =1)
            gocmax[ind:ind+12] = (w)
            ind = ind+12
            
        axs[x].plot(td,gocmean, label = 'mean (NOT VOLUME WEIGHTED \n JUST SIMPLE MEAN OF ARRAY)')
        axs[x].plot(td,gocmax, label = 'max')
        axs[x].set_yscale('log')
        axs[x].set_title(tvar)
        
        axs[0].legend(loc = 'best', fontsize = 10)
    fig.suptitle(f'{tr} (blue mean value, orange max value)')
    plt.tight_layout()
    plt.show()
    fig.savefig(f'{sdir}/SANITYCHECK_{tr}_{tmin}-{tmax}.png')