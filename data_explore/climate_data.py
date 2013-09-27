import datetime
import numpy as np


def fix_dtype(dtype):
    """Create a corrected dtype sequence from an auto-generated one.
    """
    new_dtype = []
    for name, cdtype in dtype.descr:
        int_cols = ('Year', 'Month', 'Day')
        str_cols = ('Data_Quality', 'Weather', 'Spd_of_Max_Gust_kmh')
        if name in int_cols:
            cdtype = np.int
        if name in str_cols or name.endswith('_Flag'):
            cdtype = (np.str, 30)
        if name == 'DateTime':
            cdtype = datetime.datetime
        if name == 'Time':
            cdtype = datetime.time
        if name == 'Rel_Hum_':
            name = 'Rel_Hum'
        name = name.replace('\xb0', 'deg')
        new_dtype.append((name, cdtype))
    return new_dtype


def read_climate_file(filename, delimiter='","', hourly=True, daily=False):
    """Read an Environment Canada climate data CSV file and return its data.
    """
    if hourly:
        skiprows = 16
    if daily:
        skiprows = 23
    data = np.genfromtxt(
        filename, delimiter=delimiter, skiprows=skiprows, names=True)
    new_dtype = fix_dtype(data.dtype)
    data = np.genfromtxt(
        filename, delimiter=delimiter, skiprows=skiprows+1, dtype=new_dtype)
    return data[1:]
