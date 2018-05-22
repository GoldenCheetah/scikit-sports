"""
==============================
Compute a record power profile
==============================

This example illustrates the usage of :class:`sksports.Rider` to compute
easily record power-profile,

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

##############################################################################
# The different power-profile for the activities can be plotted as follow

import matplotlib.pyplot as plt

rider.power_profile_.loc['power'].plot()
plt.xlabel('Time')
plt.ylabel('Power (W)')

###############################################################################
# Once that the power-profile for each activity are computed, we can compute
# the record power-profile for the rider and plot it.

rider.record_power_profile()['power'].plot(alpha=0.5,
                                           style='--',
                                           legend=True)
plt.xlabel('Time')
plt.ylabel('Power (W)')

plt.show()
