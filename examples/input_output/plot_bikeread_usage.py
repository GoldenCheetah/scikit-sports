"""
============================
Input/Output of cycling data
============================

This example illustrates the usage of :func:`sksports.io.bikeread` to read
cycling data. We also show how to export the data using pandas.

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

ride = bikeread(filename_fit)
print('The ride is the following:\n {}'.format(ride.head()))

###############################################################################
# :func:`sksports.io.bikeread` returns a pandas DataFrame. Thus, this is
# possible to export it in different format. We will use CSV format in this
# case.

filename_export = 'ride_exported.csv'
ride.to_csv(filename_export)

###############################################################################
# Then, it is always possible to read the file exported using pandas

import pandas as pd

ride_exported = pd.read_csv(filename_export, index_col=0, parse_dates=True)
print('The ride exported and loaded is the following:\n {}'
      .format(ride_exported.head()))

###############################################################################
# Some cleaning

import os
os.remove(filename_export)  # remove the file
