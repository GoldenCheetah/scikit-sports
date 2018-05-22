"""
=====================================
Compute Power-Profile for an Activity
=====================================

This example shows how to compute the power-profile of a cyclist for a single
activity. We will also show how to plot those information.

"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

print(__doc__)

###############################################################################
# First, we will load an activity from the toy data set available in
# scikit-sports.

from sksports.datasets import load_fit
from sksports.io import bikeread

ride = bikeread(load_fit()[0], drop_nan='columns')

###############################################################################
# We will only select some of interesting information
columns_selected = ['power', 'speed', 'cadence']
ride = ride[columns_selected]

###############################################################################
# The power-profile is extracted from the ride. By default, the maximum
# duration corresponds to the duration of the ride. However, to limit the
# processing, we limit the extraction to 8 minutes.

from sksports.extraction import activity_power_profile

power_profile = activity_power_profile(ride, '00:08:00')
print('The power-profile is:\n {}'.format(power_profile))

###############################################################################
# The power_profile is a pandas Series with multi-index. The additional
# information (e.g. speed, cadence, etc.) associated with the maximum power
# extracted are also computed. It is possible to plot those information using
# pandas. For instance, we will plot only the power information.

import matplotlib.pyplot as plt

power_profile.loc['power'].plot(title='Power-profile')
plt.xlabel('Time')
plt.ylabel('Power (W)')

###############################################################################
# In the same manner, we could plot all information using the pandas API.

power_profile.unstack().T.plot(title='Power-profile and associated variable.')
plt.xlabel('Time')

plt.show()
