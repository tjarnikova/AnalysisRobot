import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys
import copy
import glob
import os
import pandas as pd

plt.rcParams.update({'font.size': 12})
font = {'family' : 'normal',
'weight' : 'normal',
'size'   : 12}
plt.rc('font', **font)

#### add the directory for the scripts, import list of models 
sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/WORKSCRIPTS')
sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/')
import cflx as cflx
import cflxPlotr as cP
import logr as log
import lom as lom
import summarymap as smap

def runAnalysisRobot(ourModels):
    
    #endyear for cflx plots
    endyear = 2050; endatm = 550
    
    tlog = log.initLog()
    w = pd.read_csv(ourModels)
    for i in range(0,len(w['model'])):
        tnam = (w['model'][i]); syear = (w['yearstart'][i]); eyear = (w['yearend'][i])
        
        print(f'analyzing {tnam}, {syear}-{eyear}')
        #write that analysis has been started for this model for this 
        log.writeLog(tnam, syear, eyear, lognam = tlog)
        ## set up place to store plots, assign colour
        tms, yst, yen, ls, cols, resdir = log.setupVarsAndStorageDir(tnam, syear, eyear)
        
        ## make a summary map
        try:
            rawdir = lom.mod[tnam]['basedir']
            smap.make_summaryplot(tnam, rawdir, syear, eyear)
            log.noteLog('summary maps A01 rendered', lognam = tlog)
        except:
            print('something')
            log.noteLog('summary maps A01 NOT rendered', lognam = tlog)
            
        ## make the cflx plots
        try:
            print('*** CFLX analysis initialized ***')
            cflx.breakdown_maker(tnam, fmi = syear, fmx = eyear, resDir = resdir)
            print('*** PLOTTING initialized')
            dsets = []
            for i in range(0,len(tms)):
                tm = tms[i];
                ds = xr.open_dataset(glob.glob(f'/gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots/{tm}/CFLX*{tm}*.nc')[0])
                dsets.append(ds); fnam = f'B01_CFLX_plot.jpg'
            tdir = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{tnam}'
            cP.plot_carbon(dsets, cols, tms, ls, tdir, fnam, tstart=1948, tend=endyear, tendatm=endatm)
            log.noteLog('summary cflx B01 rendered', lognam = tlog)
        except:
            log.noteLog('summary cflx B01 NOT rendered', lognam = tlog)