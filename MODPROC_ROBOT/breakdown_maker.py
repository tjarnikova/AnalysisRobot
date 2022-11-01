import xarray as xr
import time
import glob
import re
import numpy as np

def breakdown_maker(tr, baseDir = '/gpfs/afm/greenocean/software/runs/', \
    forcedmin = False, fmi = 0, fmx = 3000, cflx = True, pco2 = True, exp = True, 
    salt = True, pprod = True, dic = True, verbose = False):

    '''
    for a given model, save the following diagnostics:
    cflx = 'True': carbon flux (pg/year)'

    '''
    w = time.time()
    #--------------find max and min years in TS, announce intent of where things will end up being
    tmin, tmax = max_min_yrs(tr, baseDir)
    # if we've set forced maxes and mins for start and end years, read them in here to overwrite the above
    if fmi > 0: 
        tmin = fmi;
    if fmx < 3000: 
        tmax = fmx;
    yrs = np.arange(tmin, tmax+1,1)
    print(f'BEEP BOOP RUNNING SUMMARY PROTOCOL ON MODEL {tr}')
    print(f'analyzing years {tmin}-{tmax}')
    fnam = f'SUMMARY_{tr}_{tmin}-{tmax}.nc'
    sdir = '/gpfs/home/mep22dku/scratch/SOZONE/MODPROC_ROBOT/CUSTOM_BD/'
    print(f'producing summary stats {fnam}')
    print(f'for storage in {sdir}')
    ##arrays of zeros for our things
    cflx_pg_yr = np.zeros_like(yrs)
    cflx_pg_yr_so = np.zeros_like(yrs)
    pco2_uatm_yr = np.zeros_like(yrs)
    pco2_uatm_yr_so = np.zeros_like(yrs)
    
    #--------------------open the meshmask file
    tmesh = xr.open_dataset('/gpfs/data/greenocean/software/resources/regrid/mesh_mask3_6.nc')
    

    #------------------------open DIAD
    t_yearlist = make_yearlist(tmin,tmax,'diad',tr, baseDir)
    t_ds = xr.open_mfdataset(t_yearlist)
    
    #-------------- cflx extract--------------
    if cflx:
        #cflx is in mol/m2/s, multiply by m2 in meshmask to get mol/s/grid cell
        tmesh['csize'] = tmesh.tmask[0,0,:,:] * tmesh.e1t[0,:,:] * tmesh.e2t[0,:,:]
        cflx_mol_s = t_ds['Cflx']*tmesh['csize']
        #get a yearly mean in mol_s_gridcell- takes monthly data, gets out yearly data
        t_yearly = weighted_temporal_mean(cflx_mol_s)
        siy = 60*60*24*365 #seconds in year
        pg_in_mol = 12 * 1e-15 #petagrams in a mol
        cflx_pg_yr = (np.nansum(np.nansum(t_yearly*siy*pg_in_mol, axis = 2), axis = 1))
        
        
        #southern ocean
        tmesh['csize'] = tmesh.tmask[0,0,:,:] * tmesh.e1t[0,:,:] * tmesh.e2t[0,:,:]
        cflx_mol_s = t_ds['Cflx']*tmesh['csize']
        #get a yearly mean in mol_s_gridcell- takes monthly data, gets out yearly data
        t_yearly = weighted_temporal_mean(cflx_mol_s[:,0:37,:])
        siy = 60*60*24*365 #seconds in year
        pg_in_mol = 12 * 1e-15 #petagrams in a mol
        cflx_pg_yr_so = (np.nansum(np.nansum(t_yearly*siy*pg_in_mol, axis = 2), axis = 1))
        
        if verbose:
            print(f'cflx_pg_yr: {cflx_pg_yr}')
            print(f'cflx_pg_yr_so: {cflx_pg_yr_so}')
    
    #--------------------------pco2 extract
    if pco2:
        t_yearly = weighted_temporal_mean(t_ds['pCO2'])
        glob_mean = masked_average(t_yearly, dim=['y','x'], weights=tmesh['csize'])
        pco2_uatm_yr = (glob_mean.values)
        glob_mean = masked_average(t_yearly[:,0:37,:], dim=['y','x'], weights=tmesh['csize'][0:37,:])
        pco2_uatm_yr_so = (glob_mean.values)  
    t_ds.close() 
    
    #-----------------put it all in a dataset
    ds2 = xr.Dataset(
        {
            "cflx": (["time"], cflx_pg_yr, {"units": "pg/yr"}, {"notes": "co2 flux, whole ocean"}),
            "cflx_so": (["time"], cflx_pg_yr_so, {"units": "pg/yr"}, {"notes": "co2 flux, southern ocean south of -50"}),
            "pco2": (["time"], pco2_uatm_yr, {"units": "uatm"}, {"notes": "surface pco2, whole ocean"}),
            "pco2_so": (["time"], pco2_uatm_yr_so, {"units": "uatm"}, {"notes": "surface pco2, southern ocean south of -50"}),

        },
        coords={
            "yrs": (["time"], yrs)
        },
        attrs=dict(description="model analytics"),
    )
    ds2.to_netcdf(f'{sdir}{fnam}')
        
    w2 = time.time()
    print(f'compute complete, time taken (s): {w2-w}')


def make_yearlist(yrst, yrend, dtype, tr, baseDir):
    yrs = np.arange(yrst,yrend+1,1)
    ylist = []
    for i in range(0,len(yrs)):
        ty = f'{baseDir}/{tr}/ORCA2_1m_{yrs[i]}*{dtype}*.nc'
        t2 = glob.glob(ty)
        #print(t2)
        ylist.append(t2[0])
    return ylist

def max_min_yrs(tr, baseDir):
    '''manually find the start and end year of a list of model output 
    for a given run, assuming that ptrc is being output
    needs tr - run name
    baseDir - run directory
    '''
    
    w = glob.glob(f'{baseDir}{tr}/ORCA2_1m_*ptrc*.nc')
    yrs = []
    for i in range(0,len(w)):
        ts = (w[i])
        pattern = f'{baseDir}{tr}/ORCA2_1m_'
        mod_string = re.sub(pattern, '', ts)
        yrs.append(int(mod_string[0:4]))
        
    tmin = min(yrs); tmax = max(yrs)
    return tmin, tmax


def weighted_temporal_mean(tvar):
    """
    weight by days in each month - get a yearly mean value for a quantity
    https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/
    original had stuff about nans, we don't
    """
    # Determine the month length
    month_length = tvar.time_counter.dt.days_in_month

    # Calculate the weights
    wgts = month_length.groupby("time_centered.year") / month_length.groupby("time_centered.year").sum()

    # Make sure the weights in each year add up to 1
    np.testing.assert_allclose(wgts.groupby("time_centered.year").sum(xr.ALL_DIMS), 1.0)

    # Subset our dataset for our variable
    obs = tvar

    # Calculate the numerator annual
    obs_sum = (obs * wgts).resample(time_counter="A").sum(dim="time_counter")

    return obs_sum 

def masked_average(xa:xr.DataArray,
                   dim=None,
                   weights:xr.DataArray=None,
                   mask:xr.DataArray=None):
    """
    This function will average
    :param xa: dataArray
    :param dim: dimension or list of dimensions. e.g. 'lat' or ['lat','lon','time']
    :param weights: weights (as xarray)
    :param mask: mask (as xarray), True where values to be masked.
    :return: masked average xarray
    """
    #lest make a copy of the xa
    xa_copy:xr.DataArray = xa.copy()

    if mask is not None:
        xa_weighted_average = __weighted_average_with_mask(
            dim, mask, weights, xa, xa_copy
        )
    elif weights is not None:
        xa_weighted_average = __weighted_average(
            dim, weights, xa, xa_copy
        )
    else:
        xa_weighted_average =  xa.mean(dim)

    return xa_weighted_average



    # %% [markdown]
def __weighted_average(dim, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
    x_times_w = xa_copy * weights_all_dims
    xw_sum = x_times_w.sum(dim)
    x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
    xa_weighted_average = xw_sum / x_tot
    return xa_weighted_average


def __weighted_average_with_mask(dim, mask, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, mask_all_dims = xr.broadcast(xa, mask)  # broadcast to all dims
    xa_copy = xa_copy.where(np.logical_not(mask))
    if weights is not None:
        _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
        weights_all_dims = weights_all_dims.where(~mask_all_dims)
        x_times_w = xa_copy * weights_all_dims
        xw_sum = x_times_w.sum(dim=dim)
        x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
        xa_weighted_average = xw_sum / x_tot
    else:
        xa_weighted_average = xa_copy.mean(dim)
    return xa_weighted_average


# ## Application 1: Weigted global average:
# Grid cells have different area, so when we do the global average, they have to be weigted by the area of each grid cell.
# Here we do it for 2 m temperature: