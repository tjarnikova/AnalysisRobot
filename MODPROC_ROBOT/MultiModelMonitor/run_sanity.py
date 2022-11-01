#-----IMPORTS
import matplotlib.pyplot as plt
import glob
import xarray as xr
import sys
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/MODPROC_ROBOT/MultiModelMonitor/WORK_SCRIPTS')
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/MO_pipeline/')
import scendict as sc
import bio_sanity as bs
 
#------CHANGE THIS TO WHAT YOU WANT TO EXTRACT
extract = True # run it?

sdir = '/gpfs/home/mep22dku/scratch/SOZONE/MODPROC_ROBOT/MultiModelMonitor/OUTPUT/' #results directory
tms = ['TOM12_DW_WE43']#, 'TOM12_TJ_1BS3' ]#,'TOM12_TJ_1BS2', 'TOM12_TJ_3AS1','TOM12_DW_WE43', 'TOM12_DW_GA01'] ##models to plot
baseDir = '/gpfs/afm/greenocean/software/runs/'

if extract: 
    for tm in tms:
        print(f'running sanity check for {tm}')
        bs.get_sanity(tm, baseDir,sdir)

