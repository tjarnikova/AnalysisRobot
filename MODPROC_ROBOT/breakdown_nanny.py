## read breakdowns
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter


parser = argparse.ArgumentParser(description=  """   
    script for quickly visualizing breakdowns - labels may need changing
    """, formatter_class=RawTextHelpFormatter)

parser.add_argument('modnam', default='test_model', help='model name')
#read in variables and convert as necessary to int
args=parser.parse_args()
modname = args.modnam

#tr = 'TOM12_TJ_M001'
tr = modname
rd = '/gpfs/home/mep22dku/scratch/ModelRuns/'
tfs = ['sur','lev','vol','ave']
labs = ['Cflx,PgCarbonPerYr','EXP PgCarbonPerYr','PPT,PgCarbonPerYr','Avg:TChl','']
fact = 0.4
fig, axs = plt.subplots(2,2, figsize=(20*fact, 14*fact), facecolor='w', edgecolor='k')
axs = axs.ravel()

for i in range(0,4):

    tf = tfs[i]; lab = labs[i]
    df = pd.read_csv(f'{rd}{tr}/breakdown.{tf}.annual.dat',sep='\t',skiprows=3, header=None)
    # w.columns = head
    #year and first total
    axs[i].plot(df.iloc[:,0],df.iloc[:,1])
    axs[i].set_title(lab)

fig.suptitle(f'Whole-domain values from breakdown, {tr}')
fig.savefig(f'{tr}_breakdown_nanny.jpg')
plt.tight_layout()