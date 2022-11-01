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


fact = 0.4
fig, axs = plt.subplots(2,1, figsize=(20*fact, 6*fact), facecolor='w', edgecolor='k')
axs = axs.ravel()
axs[0].plot(yrs, indarray, 'ro')
axs[0].set_title('Does model salinity look ok? \n 0=numbers where expected, 1 = nans in model, 2 = file not present')
axs[0].set_title('Diagnostic - Does model salinity look ok? \n 0=numbers where expected, 1 = nans in model, 2 = file not present')


plt.tight_layout()
for i in range(0,1):
    axs[i].grid()
    axs[i].legend()
    axs[i].set_xlim([yrstart,yrend])
fig.savefig(f'Linemonitor_{modname}.jpg')