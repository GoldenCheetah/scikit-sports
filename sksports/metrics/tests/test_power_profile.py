"""Test the metrics linked to the power profile."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from os.path import dirname, join

import pandas as pd
import pytest

from sksports import Rider
from sksports.metrics import aerobic_meta_model

module_path = dirname(__file__)
filename_csv = join(module_path, 'data', 'rider_power_profile.csv')
rider = Rider.from_csv(filename_csv)


@pytest.mark.parametrize(
    "rpp, ts, expected_mpa, expected_time_mpa, expected_aei",
    [(rider.record_power_profile()['power'], None,
      453.372, pd.Timedelta('00:03:00'), -11.48848),
     (rider.record_power_profile()['power'],
      pd.timedelta_range('00:00:01', '04:00:00', freq='5S'),
      444.0816, pd.Timedelta('00:03:16'), -10.99544),
     (rider.record_power_profile()['power'],
      pd.timedelta_range('00:00:01', '05:00:00', freq='5S'),
      444.0816, pd.Timedelta('00:03:16'), -10.99544)])
def test_aerobic_meta_model(rpp, ts,
                            expected_mpa,
                            expected_time_mpa,
                            expected_aei):
    mpa, time_mpa, aei, _, _ = aerobic_meta_model(rpp, ts)
    print(time_mpa)
    assert mpa == pytest.approx(expected_mpa)
    assert time_mpa == expected_time_mpa
    assert aei == pytest.approx(expected_aei)
