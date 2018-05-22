"""
==================================
Store and load rider power-profile
==================================

This example illustrates how to store the information contained in a
:class:`sksports.Rider` instance.

"""

print(__doc__)

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

###############################################################################
# We will use the :class:`sksports.Rider` class to compute power-profile for
# the toy data sets.

from sksports.datasets import load_fit
from sksports import Rider

rider = Rider()
rider.add_activities(load_fit())

print('The computed activities are:\n {}'.format(rider.power_profile_))

###############################################################################
# We can store and load the information using the `to_csv` and `from_csv`
# methods.

filename_rider = 'rider.csv'
rider.to_csv(filename_rider)

rider_reloaded = Rider.from_csv(filename_rider)

###############################################################################
# Clean the temporary csv file
import os
os.remove(filename_rider)
