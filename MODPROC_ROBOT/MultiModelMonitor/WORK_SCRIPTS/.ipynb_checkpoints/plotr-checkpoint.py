import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

def plot_carbon(dsets, cols, descs, ls, sdir, fnam, tstart = 1948, tend = 2100, tendatm = 800):
    fact = 0.7
    fig, axs = plt.subplots(2,2, figsize=(23*fact, 14*fact), facecolor='w', edgecolor='k')
    axs = axs.ravel()

    ### cflx total
    for i in range(0,len(dsets)):
        ds = dsets[i]; col = cols[i]
        axs[0].plot(ds.yrs, ds.cflx, color = col, label = descs[i], linestyle = ls[i])
        axs[1].plot(ds.yrs, ds.cflx_so, color = col, linestyle = ls[i])
        axs[2].plot(ds.yrs, ds.pco2, color = col, linestyle = ls[i])
        axs[3].plot(ds.yrs, ds.pco2_so, color = col, label = descs[i], linestyle = ls[i])

    tits = ['air-sea CO2 flux, whole domain', 'air-sea CO2 flux, SO south of -50',\
            'surface pCO2, whole domain', 'surface pCO2, SO south of -50']
    ylabs = ['petagram C', 'petagram C', '$\mu$atm', '$\mu$atm']
    for i in range(0,4):
        axs[i].grid()
        axs[i].set_xlim(tstart,tend)
        axs[i].set_title(tits[i])
        axs[i].set_ylabel(ylabs[i])

    axs[2].set_ylim([280,tendatm])
    axs[3].set_ylim([280,tendatm])

    axs[3].legend(loc = 'best', fontsize = 11)
    fig.savefig(f'{sdir}{fnam}')
    
    