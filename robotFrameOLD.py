### specify what you want the robot to do 
ourModels = 'modelsToAnalyze.txt'
tlog = 'RobotLog.txt'
PLOT = True ##for each type of analysis, make the relevant plot
CFLX = True; # extract cflx 
endyear = 2015; endatm = 450 ## 

#### import stuff 
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys
import warnings
warnings.filterwarnings('ignore')
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

w = pd.read_csv(ourModels)
for i in range(0,len(w['model'])):
    tnam = (w['model'][i])
    syear = (w['yearstart'][i])
    eyear = (w['yearend'][i])
    print(f'analyzing {tnam}')
    
    ##write logs etc
    log.write_log(tnam, syear, eyear, PLOT, CFLX, lognam = tlog)
    tms, yst, yen, ls, cols, resdir = log.setupVarsAndStorageDir(tnam, syear, eyear)
    
    ### cflx analysis
    if CFLX:
        print('*** CFLX analysis initialized ***')
        cflx.breakdown_maker(tnam, fmi = syear, fmx = eyear, resDir = resdir)
        print('*** PLOTTING initialized')
        if PLOT: 
            dsets = []
            for i in range(0,len(tms)):
                tm = tms[i];
                ds = xr.open_dataset(glob.glob(f'/gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots/{tm}/CFLX*{tm}*.nc')[0])
                dsets.append(ds); fnam = f'CFLX_plot_{tm}.jpg'
            cP.plot_carbon(dsets, cols, tms, ls, resdir, fnam, tstart=1948, tend=2015, tendatm=450)
    
    
    print('')