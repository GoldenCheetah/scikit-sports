"""Test the power package which model power using aside data."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import pytest

import numpy as np
from numpy.testing import assert_array_less
from numpy.testing import assert_allclose

import pandas as pd
from pandas.testing import assert_series_equal

from sksports.model import strava_power_model
from sksports.extraction import gradient_elevation
from sksports.extraction import acceleration
from sksports.exceptions import MissingDataError


speed = np.ones(100) * 5
distance = np.linspace(0, 99, num=100)
elevation = np.linspace(0, 9, num=100)
activity = pd.DataFrame({'speed': speed,
                         'distance': distance,
                         'elevation': elevation})


@pytest.mark.parametrize(
    "activity_corrupted, use_acceleration",
    [(activity.copy().drop(columns='distance'), False),
     (activity.copy().drop(columns='speed'), True)]
)
def test_strava_power_model_error(activity_corrupted, use_acceleration):
    with pytest.raises(MissingDataError):
        strava_power_model(activity_corrupted, cyclist_weight=70,
                           use_acceleration=use_acceleration)


def test_strava_power_model_auto_compute():
    # check that the acceleration and the elevation will be auto-computed
    power_auto = strava_power_model(activity, cyclist_weight=70)

    activity_ele_acc = activity.copy()
    activity_ele_acc = gradient_elevation(activity)
    activity_ele_acc = acceleration(activity_ele_acc)
    power_ele_acc = strava_power_model(activity_ele_acc, cyclist_weight=70)

    assert_series_equal(power_auto, power_ele_acc)


def test_strava_power_model():
    # at constant speed the acceleration should not have any influence
    power_without_acc = strava_power_model(activity, cyclist_weight=78,
                                           use_acceleration=False)
    power_with_acc = strava_power_model(activity, cyclist_weight=78,
                                        use_acceleration=True)
    assert_allclose(power_without_acc, power_with_acc)

    # increase cyclist weight should increase power
    power_initial = strava_power_model(activity, cyclist_weight=70)
    power_increase_weight = strava_power_model(activity, cyclist_weight=78)
    assert_array_less(power_initial, power_increase_weight)

    # increase bike weight should increase power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       bike_weight=7)
    power_increase_weight = strava_power_model(activity, cyclist_weight=70,
                                               bike_weight=8)
    assert_array_less(power_initial, power_increase_weight)

    # increase the rolling coefficient should increase power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       coef_roll_res=0.0045)
    power_increase_cr = strava_power_model(activity, cyclist_weight=70,
                                           coef_roll_res=0.006)
    assert_array_less(power_initial, power_increase_cr)

    # increase of the pressure should increase power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       pressure=101325)
    power_increase_pressure = strava_power_model(activity, cyclist_weight=70,
                                                 pressure=110000)
    assert_array_less(power_initial, power_increase_pressure)

    # decrease the temperature should increase the power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       temperature=15.0)
    power_decrease_temperature = strava_power_model(activity,
                                                    cyclist_weight=70,
                                                    temperature=10.0)
    assert_array_less(power_initial, power_decrease_temperature)

    # increase the drag coefficient should increase the power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       coef_drag=0.5)
    power_increase_coef_drag = strava_power_model(activity,
                                                  cyclist_weight=70,
                                                  coef_drag=1.0)
    assert_array_less(power_initial, power_increase_coef_drag)

    # increase the rider frontal surface should increase the power
    power_initial = strava_power_model(activity, cyclist_weight=70,
                                       surface_rider=0.32)
    power_increase_surface_rider = strava_power_model(activity,
                                                      cyclist_weight=70,
                                                      surface_rider=0.5)
    assert_array_less(power_initial, power_increase_surface_rider)
