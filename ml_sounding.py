import matplotlib.pyplot as plt
import pandas as pd
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import Hodograph, SkewT
from metpy.units import units

def read_skewT(sounding_file):
    col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']
    df = pd.read_fwf(sounding_file,skiprows=1, usecols=[0, 1, 2, 3, 6, 7], names=col_names)
    return df

#Modify this to match your sounding file name
sounding_file = '/Users/ethan1/Desktop/vs_code/NSSL/BUF202302180000Z.txt'
#Call function to read in sounding data
df = read_skewT(sounding_file)
#Extract variables for sounding
p = df['pressure'].values * units.hPa
T = df['temperature'].values * units.degC
Td = df['dewpoint'].values * units.degC
wind_speed = df['speed'].values * units.knots
wind_dir = df['direction'].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir)

#Supplementary calculations
parcel_prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
rh = mpcalc.relative_humidity_from_dewpoint(T,Td)
lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])

fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig, rotation=30)

skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)

# skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
# skew.plot(p, parcel_prof, 'k', linewidth=2)

# skew.shade_cin(p, T, parcel_prof, Td)
# skew.shade_cape(p, T, parcel_prof)

skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

skew.ax.set_xlim(-60, 20)

skew.ax.set_ylabel("Pressure [hPa]")
skew.ax.set_xlabel("Temperature [°C]")
skew.ax.set_title('BUF202302180000Z', fontsize = 20, fontweight = 'bold')

plt.show()