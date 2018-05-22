# coding: utf-8

"""
=======================================
Quantify Effort in Activity using Power
=======================================

This example illustrates which metrics can be used to quantify the effort of a
cyclist during a cycling ride.

"""

print(__doc__)

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

###############################################################################
# We can first read a toy ride from the library

from sksports.datasets import load_fit
from sksports.io import bikeread

ride = bikeread(load_fit()[0])

###############################################################################
# Different scores are available in ``scikit-sports``. We can first compute
# the normalized power® which corresponds to an average power during the ride
# with an additional smoothing. To compute this score, we need to know the
# maximum power aerobic (or the functional threshold power).

from sksports.metrics import normalized_power_score

mpa = 400
np_score = normalized_power_score(ride['power'], mpa)
print('Normalized power {:.2f}'.format(np_score))

###############################################################################
# The intensity factor® normalize the normalized power using the functional
# threshold power.

from sksports.metrics import intensity_factor_score

if_score = intensity_factor_score(ride['power'], mpa)
print('Intensity factor {:.2f}'.format(if_score))

###############################################################################
# To obtain a metric which is normalized depending of the time, we need to
# compute the training stress score® which is derived from the intensity
# factor®.

from sksports.metrics import training_stress_score

ts_score = training_stress_score(ride['power'], mpa)
print('Training stress score {:2f}'.format(ts_score))

###############################################################################
# Alternatively, we can use the ESIE scale to compute the load of an activity.

from sksports.metrics import training_load_score

tl_score = training_load_score(ride['power'], mpa)
print('Training load score {:.2f}'.format(tl_score))
