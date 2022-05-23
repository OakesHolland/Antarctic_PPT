## Particle backtracking example from Casey Station, Antarctica 
## Uses Python OpenDrift software package
## https://opendrift.github.io/

from datetime import datetime, timedelta
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic
import numpy as np
import opendrift
import os

o = OceanDrift(loglevel = 20)


currents = reader_netCDF_CF_generic.Reader('https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0')
wind = reader_netCDF_CF_generic.Reader('https://pae-paha.pacioos.hawaii.edu/thredds/dodsC/ncep_global/NCEP_Global_Atmospheric_Model_best.ncd')
stokes = reader_netCDF_CF_generic.Reader('/local_stokes_files.nc')

## At time of processing there were no thredds readers for stokes drift. 
## Stokes drift data used: Global analysis forecast wav_001_027
## Downloaded from: https://resources.marine.copernicus.eu/products


o.add_reader([currents, wind, stokes])

wind_drift_factor = np.random.uniform(0.01, 0.03, 1000000)

autumn = datetime(2020,4,15,0,0)
  
o.seed_elements(lon = 110.52,
    lat = -66.28,
    radius = 100,
    number = 1000000,
    wind_drift_factor = wind_drift_factor,
    time = autumn)
   
o.set_config('drift:current_uncertainty', 0.1)
o.set_config('drift:wind_uncertainty', 0.1)
o.set_config('drift:advection_scheme', 'runge-kutta4')
o.set_config('general:coastline_action', 'previous')
o.set_config('drift:vertical_mixing', False)

ofile = 'casey_backtrack.nc'
fname = 'casey_backtrack.jpg'
aname = 'casey_backtrack.mp4'

o.run(time_step = timedelta(hours = -3),
    duration = timedelta(days = 365),
    time_step_output = timedelta(days = 7),
    outfile = ofile)    
  
o.plot(legend = True,
    fast = False,
    filename = fname)  
    
o.animation(fast = False,
    filename = aname)  
    
