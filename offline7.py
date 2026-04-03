## Note that in this code, I output only a specific area of model output. As a result, the lat
## and lon becomes LAT_10n_to_40n and LON_0e_to_360e

# import package and functions
import numpy as np
import climlab
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import glob,os
from Transfer_longitude import *
from Offline_RRTMG import *

path="/.../SST_only/run/"
dss_year=glob.glob(os.path.join(path, "SST_only.cam.h2.*-07-*-*.nc"))

for k in range(10): ## years

    dss=dss_year[k*31:(k+1)*31]

    # Get the number of days in a month
    length=len(dss)
    num_day=length
    
    # Do the offline calculation for every time in every day
    for day in range(num_day): ## all days in the month
        filepath=dss[day]
        fi   =xr.open_dataset(filepath)

        # First, rename the longitude and latitude
        fi_temp=fi.rename({'LON_0e_to_360e':'lon','LAT_10n_to_40n':'lat'})

        ## Transfer the longitude
        temp=central180_to_0(fi_temp)

        # Find the area of the Sahara Desert
        i_start,=np.where(np.isclose(temp.lon, -30))
        i_end,=np.where(np.isclose(temp.lon, 45))
        j_start,=np.where(np.isclose(temp.lat, 18))
        j_end,=np.where(np.isclose(temp.lat, 35.052632))

        # Create an array to store the data
        data_lwcon =temp.CFC12_rad_LON_0e_to_360e_LAT_10n_to_40n.copy()
        data_swcon =temp.CFC12_rad_LON_0e_to_360e_LAT_10n_to_40n.copy()
        data_lwup  =temp.TINT_LON_0e_to_360e_LAT_10n_to_40n.copy()
        data_lwdown=temp.TINT_LON_0e_to_360e_LAT_10n_to_40n.copy()
        data_swup  =temp.TINT_LON_0e_to_360e_LAT_10n_to_40n.copy()
        data_swdown=temp.TINT_LON_0e_to_360e_LAT_10n_to_40n.copy()

        # calculate for all grid points and time
        time=temp.time
        lat_range=temp.lat
        lon_range=temp.lon

        # Do the calculation for every grid point
        for t in range(0,len(time)): ## hour
            for j in range(int(j_start),int(j_end)+1):
                for i in range(int(i_start),int(i_end)+1):
                    Input=gcm_data(temp,t,j,i)
                    lw_up,lw_down,lw_con,sw_up,sw_down,sw_con=offline(Input.nlay,Input.plev,Input.play,Input.tsfc,Input.tlev,Input.tlay,\
                                      Input.h2ovmr,Input.o3vmr,Input.co2vmr,Input.ch4vmr,Input.n2ovmr,Input.cfc11vmr,\
                                      Input.cfc12vmr,Input.o2vmr,Input.cfc22vmr,Input.ccl4vmr,Input.cldfrac,\
                                      Input.ciwp, Input.clwp, Input.reic, Input.relq, Input.asdir, Input.asdif, Input.aldir, \
                                      Input.aldif,Input.coszen,Input.eccf,Input.ilev,Input.mlev)
                    data_lwcon[t,:,j,i]  =lw_con
                    data_lwup[t,:,j,i]   =lw_up
                    data_lwdown[t,:,j,i] =lw_down
                    data_swcon[t,:,j,i]  =sw_con
                    data_swup[t,:,j,i]   =sw_up
                    data_swdown[t,:,j,i] =sw_down

        # Combine the data from all days
        if day==0:
            lwcon =data_lwcon
            lwup  =data_lwup
            lwdown=data_lwdown
            swcon =data_swcon
            swup  =data_swup
            swdown=data_swdown
        else:
            lwcon =xr.concat([lwcon,data_lwcon],dim="time")
            lwup  =xr.concat([lwup,data_lwup],dim="time")
            lwdown=xr.concat([lwdown,data_lwdown],dim="time")
            swcon =xr.concat([swcon,data_swcon],dim="time")
            swup  =xr.concat([swup,data_swup],dim="time")
            swdown=xr.concat([swdown,data_swdown],dim="time")
        
    # Do the monthly average
    lw_con_mm =lwcon.mean(dim='time')
    lw_up_mm  =lwup.mean(dim='time')
    lw_down_mm=lwdown.mean(dim='time')
    sw_con_mm =swcon.mean(dim='time')
    sw_up_mm  =swup.mean(dim='time')
    sw_down_mm=swdown.mean(dim='time')

    # Write the data
    lw_up_mm.to_netcdf("/.../lwup_7_"+str(k+1979)+".nc")
    lw_down_mm.to_netcdf("/.../lwdown_7_"+str(k+1979)+".nc")
    sw_up_mm.to_netcdf("/.../swup_7_"+str(k+1979)+".nc")
    sw_down_mm.to_netcdf("/.../swdown_7_"+str(k+1979)+".nc")
    # lw.to_netcdf("/zhoulab_rit/lzhuo/data/offline_con/lwcon_6_"+str(k+1979)+".nc")
    # sw.to_netcdf("/zhoulab_rit/lzhuo/data/offline_con/swcon_6_"+str(k+1979)+".nc")
    # lw.to_netcdf("/zhoulab_rit/lzhuo/data/offline_con/lwcon_6_"+str(k+2011)+".nc")
    # sw.to_netcdf("/zhoulab_rit/lzhuo/data/offline_con/swcon_6_"+str(k+2011)+".nc")
