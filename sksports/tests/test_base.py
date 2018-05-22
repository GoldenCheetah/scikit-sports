# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import os
import shutil
from tempfile import mkdtemp

import pytest
from pandas.testing import assert_frame_equal

from sksports.base import Rider
from sksports.datasets import load_fit
from sksports.datasets import load_rider


def test_rider_add_activities_update():
    rider = Rider.from_csv(load_rider())
    rider.delete_activities('07 May 2014')
    rider.add_activities(load_fit()[0])
    assert rider.power_profile_.shape == (35771, 3)

    with pytest.raises(ValueError, message='activity was already added'):
        rider.add_activities(load_fit()[0])


@pytest.mark.parametrize(
    "rider, filename, expected_shape",
    [(Rider(), load_fit(), (40218, 3)),
     (Rider(), load_fit()[0], (13536, 1))])
def test_rider_add_activities(rider, filename, expected_shape):
    rider.add_activities(filename)
    assert rider.power_profile_.shape == expected_shape


@pytest.mark.parametrize(
    "dates, time_comparison, expected_shape",
    [('07 May 2014', False, (33515, 2)),
     ('07 May 2014', True, (33515, 3)),
     ('07 May 2014 12:26:22', True, (33515, 2)),
     (['07 May 2014'], False, (33515, 2)),
     (tuple(['07 May 2014', '11 May 2014']), False, (33515, 1))])
def test_rider_delete_activities(dates, time_comparison, expected_shape):
    rider = Rider.from_csv(load_rider())
    rider.delete_activities(dates, time_comparison=time_comparison)
    assert rider.power_profile_.shape == expected_shape


@pytest.mark.parametrize(
    "dates",
    [(tuple(['07 May 2014'])),
     (tuple(['07 May 2014', '10 May 2014', '11 May 2014']))])
def test_rider_delete_activities_error(dates):
    rider = Rider.from_csv(load_rider())

    msg = "Wrong tuple format"
    with pytest.raises(ValueError, message=msg):
        rider.delete_activities(dates)


@pytest.mark.parametrize(
    "range_dates, expected_shape",
    [(None, (6703, 5)),
     (('07 May 2014', '11 May 2014'), (3812, 5))])
def test_rider_record_power_profile(range_dates, expected_shape):
    rider = Rider.from_csv(load_rider())
    rpp = rider.record_power_profile(range_dates=range_dates)
    assert rpp.shape == expected_shape


def test_dump_load_rider():
    filenames = load_fit()[:1]
    rider = Rider()
    rider.add_activities(filenames)

    tmpdir = mkdtemp()
    csv_filename = os.path.join(tmpdir, 'rider.csv')
    try:
        rider.to_csv(csv_filename)
        rider2 = Rider.from_csv(csv_filename)
        assert_frame_equal(rider.power_profile_, rider2.power_profile_)
    finally:
        shutil.rmtree(tmpdir)
