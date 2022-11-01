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
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/MO_pipeline/')
sys.path.append('/gpfs/home/mep22dku/scratch/SOZONE/UTILS/')
import utils as ut

## code to parse command line input and provide a help description
parser = argparse.ArgumentParser(description=  """   

    Important: assumes output is in /gpfs/afm/greenocean/software/runs/
    (Else baseDir variable on line 2 of this script must be changed)
    
    command-line usage:
    python run_linemonitor.py model_run_name yearstart yearend

    written by TJSJ 2022 (T.Jarnikova@uea.ac.uk) 
    """, formatter_class=RawTextHelpFormatter)

parser.add_argument('modnam', default='test_model', help='model name')
parser.add_argument('yearstart', default=9999, help='year to analyze')
parser.add_argument('yearend', default=9999, help='year to analyze')



#read in variables and convert as necessary to int
args=parser.parse_args()
modname = args.modnam
yrstart = int(args.yearstart)
yrend = int(args.yearend)
yrs = np.arange(yrstart,yrend+1,1)

print(f'Plotting for run {modname}, years {yrstart}-{yrend}')

### extract salt and things
path_to_files = f'{baseDir}/{modname}';
ftype = 'grid_T'
var = 'vosaline'; print(var)
indarray, list_of_nanyears = ut.check_for_nans(yrstart,yrend,path_to_files,ftype,var)
storar = ut.extract_model_from_daily_3D(yrstart,yrend,path_to_files,ftype,var)
salt_0 = storar[:,:,0,:,:];
salt_0_mn = np.nanmean(np.nanmean(np.nanmean(salt_0, axis = 1), axis = 1), axis = 1)
del storar

var = 'votemper'; print(var)
storar = ut.extract_model_from_daily_3D(yrstart,yrend,path_to_files,ftype,var)
temp_0 = storar[:,:,0,:,:];
temp_0_mn = np.nanmean(np.nanmean(np.nanmean(temp_0, axis = 1), axis = 1), axis = 1)
del storar

ftype = 'ptrc_T'
var = 'DIC'; print(var)
storar = ut.extract_model_from_daily_3D(yrstart,yrend,path_to_files,ftype,var)
DIC_0 = storar[:,:,0,:,:];
DIC_0_mn = np.nanmean(np.nanmean(np.nanmean(DIC_0, axis = 1), axis = 1), axis = 1)
del storar

ftype = 'diad_T'
var = 'Cflx'; print(var)
storar = ut.extract_model_from_daily_2D(yrstart,yrend,path_to_files,ftype,var)
Clfx = storar[:,:,:,:]
Clfx_mn = np.nanmean(np.nanmean(np.nanmean(Clfx, axis = 1), axis = 1), axis = 1)
print(Clfx_mn)
del storar

fact = 0.4
fig, axs = plt.subplots(5,1, figsize=(20*fact, 22*fact), facecolor='w', edgecolor='k')
axs = axs.ravel()
axs[0].plot(yrs, indarray, 'ro')
axs[0].set_title('Does model salinity look ok? \n 0=numbers where expected, 1 = nans in model, 2 = file not present')
axs[0].set_title('Diagnostic - Does model salinity look ok? \n 0=numbers where expected, 1 = nans in model, 2 = file not present')

axs[1].plot(yrs, salt_0_mn, 'r-', label = '0m')
axs[1].set_title('Mean model salinity (3 depths)')

axs[2].plot(yrs, temp_0_mn, 'r-', label = '0m')
axs[2].set_title('Mean model temperature (3 depths)')

axs[3].plot(yrs, DIC_0_mn, 'k-', label = '0m')
axs[3].set_title('Mean model DIC (3 depths)')


axs[4].plot(yrs, Clfx_mn, 'r-', label = '0m')
axs[4].set_title('carbon air-sea flux')

plt.tight_layout()
for i in range(0,5):
    axs[i].grid()
    axs[i].legend()
    axs[i].set_xlim([yrstart,yrend])
fig.savefig(f'Linemonitor_{modname}.jpg')