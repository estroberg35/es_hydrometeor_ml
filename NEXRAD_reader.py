print(__doc__)

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# Modified by Ethan Stroberg
# License: BSD 3 clause

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pyart
import numpy as np

# open the file, create the displays and figure
filename = "NSSL/" + "KTYX20230201_185439_V06"
radar = pyart.io.read_nexrad_archive(filename)
display = pyart.graph.RadarMapDisplay(radar)

# set projection
projection = ccrs.LambertConformal(
    central_latitude = radar.latitude["data"][0],
    central_longitude = radar.longitude["data"][0],
)
# create figure
fig = plt.figure(figsize=(6, 5))
ax = plt.axes(projection = projection)

# add state lines
ax.add_feature(cfeature.STATES.with_scale("50m"), edgecolor = "black", linewidth = 0.8)

display.plot_ppi_map(
    "reflectivity",
    0,
    title="Reflectivity on Feb 1, 2023, NY",
    vmin=0,
    vmax=72,
    min_lon=-77,
    max_lon=-74,
    min_lat=43,
    max_lat=45,
    lon_lines=np.arange(-77, -74 , 0.5),
    resolution="10m",
    lat_lines=np.arange(43, 45, 0.5),
    projection=projection,
    fig=fig,
    lat_0=radar.latitude["data"][0],
    lon_0=radar.longitude["data"][0],
    colorbar_label="dBZ",
    #cmap = "NWSRef",
    ax=ax
)

# Indicate the launch location with a point
ax.plot(-76.2011, 43.8239, 'ro', markersize=6, transform=ccrs.PlateCarree())


plt.show()