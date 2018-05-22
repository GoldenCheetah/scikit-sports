"""Test the gradient module."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import numpy as np
import pandas as pd

import pytest

from sksports.extraction import acceleration
from sksports.extraction import gradient_activity
from sksports.extraction import gradient_elevation
from sksports.extraction import gradient_heart_rate
from sksports.exceptions import MissingDataError


def test_acceleration_error():
    activity = pd.DataFrame({'A': np.random.random(1000)})
    msg = "speed data are required"
    with pytest.raises(MissingDataError, message=msg):
        acceleration(activity)


@pytest.mark.parametrize(
    "activity, append, type_output, shape",
    [(pd.DataFrame({'speed': np.random.random(100)}),
      False, pd.Series, (100,)),
     (pd.DataFrame({'speed': np.random.random(100)}),
      True, pd.DataFrame, (100, 2))])
def test_acceleration(activity, append, type_output, shape):
    output = acceleration(activity, append=append)
    assert isinstance(output, type_output)
    assert output.shape == shape


def test_gradient_elevation_error():
    activity = pd.DataFrame({'A': np.random.random(1000)})
    msg = "elevation and distance data are required"
    with pytest.raises(MissingDataError, message=msg):
        gradient_elevation(activity)


@pytest.mark.parametrize(
    "activity, append, type_output, shape",
    [(pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      False, pd.Series, (100,)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      True, pd.DataFrame, (100, 3))])
def test_gradient_elevation(activity, append, type_output, shape):
    output = gradient_elevation(activity, append=append)
    assert isinstance(output, type_output)
    assert output.shape == shape


def test_gradient_heart_rate_error():
    activity = pd.DataFrame({'A': np.random.random(1000)})
    msg = "heart-rate data are required"
    with pytest.raises(MissingDataError, message=msg):
        gradient_heart_rate(activity)


@pytest.mark.parametrize(
    "activity, append, type_output, shape",
    [(pd.DataFrame({'heart-rate': np.random.random(100)}),
      False, pd.Series, (100,)),
     (pd.DataFrame({'heart-rate': np.random.random(100)}),
      True, pd.DataFrame, (100, 2))])
def test_gradient_heart_rate(activity, append, type_output, shape):
    output = gradient_heart_rate(activity, append=append)
    assert isinstance(output, type_output)
    assert output.shape == shape


@pytest.mark.parametrize(
    "activity, periods, append, columns, shape",
    [(pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      1, True, None, (100, 4)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      1, False, None, (100, 2)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      1, False, ['elevation'], (100, 1)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      [1, 2], True, None, (100, 6)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      [1, 2], False, None, (100, 4)),
     (pd.DataFrame({'elevation': np.random.random(100),
                    'distance': np.random.random(100)}),
      [1, 2], True, ['elevation'], (100, 4))])
def test_gradient_activity(activity, periods, append, columns, shape):
    output = gradient_activity(activity, periods=periods, append=append,
                               columns=columns)
    assert output.shape == shape
