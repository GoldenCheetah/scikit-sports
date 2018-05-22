"""
==================
Plot Activity Data
==================

This example shows how to plot the information read with the function
:func:`sksports.io.bikeread` using pandas.

"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

print(__doc__)

###############################################################################
# `scikit-sports` has couple of `fit` files stored which can be used as toy
# data.

from sksports.datasets import load_fit

filename_fit = load_fit()[0]  # catch the first toy file
print('The fit file which will be used is stored at: \n {}'
      .format(filename_fit))

###############################################################################
# The function :func:`sksports.io.bikeread` allows to read the file without
# any extra information regarding the format.

from sksports.io import bikeread

ride = bikeread(filename_fit, drop_nan='columns')
print('The ride is the following:\n {}'.format(ride.head()))

###############################################################################
# First, we can list the type of data available in the DataFrame

print('The available data are {}'.format(ride.columns))

###############################################################################
# Plotting a specific column (e.g. power) is easy using the pandas ``plot``
# function.

import matplotlib.pyplot as plt

ride['power'].plot(legend=True)
plt.xlabel('Time')
plt.ylabel('Power (W)')

###############################################################################
# In the same manner we can plot several column at the same time.

columns = ['power', 'speed', 'cadence', 'elevation']
ride[columns].plot(legend=True)
plt.xlabel('Time')
plt.title('Plot a subset of data')

###############################################################################
# To smooth the data, we can even resample them before to plot them

ride[columns].resample('20S').interpolate().plot(legend=True)
plt.xlabel('Time')
plt.title('Data are resample with a sampling rate of 20 seconds')

plt.show()
