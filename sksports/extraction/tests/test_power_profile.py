# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from datetime import timedelta

import pytest

from sksports.io import bikeread
from sksports.datasets import load_fit
from sksports.extraction import activity_power_profile


@pytest.mark.parametrize(
    "max_duration, power_profile_shape, first_element",
    [(None, (13536,), 8.2117765957446736),
     (10, (54,), 5.8385555555555557),
     ('00:00:10', (54,), 5.8385555555555557),
     (timedelta(seconds=10), (54,), 5.8385555555555557)]
)
def test_activity_power_profile(max_duration, power_profile_shape,
                                first_element):
    activity = bikeread(load_fit()[0])
    power_profile = activity_power_profile(activity, max_duration=max_duration)
    assert power_profile.shape == power_profile_shape
    assert power_profile.iloc[-1] == pytest.approx(first_element)


def test_activity_power_profile_max_duration_too_large():
    # test that there is no segmentation fault when max_duration is set too
    # large and that we fall back to the largest possible interval.
    activity = bikeread(load_fit()[0])
    power_profile = activity_power_profile(activity, max_duration=1000000)
    assert power_profile.shape == (13536,)
    assert power_profile.iloc[-1] == pytest.approx(8.2117765957446736)
