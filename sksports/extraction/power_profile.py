"""Extraction of information based on the power-profile."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from datetime import time, timedelta
from numbers import Integral

import numpy as np
import pandas as pd

from ._power_profile import max_mean_power_interval
from ._power_profile import _associated_data_power_profile


def activity_power_profile(activity, max_duration=None):
    """Compute the power profile for an activity.

    Read more in the :ref:`User Guide <activity_power_profile>`.

    Parameters
    ----------
    activity : DataFrame
        A pandas DataFrame with at least a ``'power'`` column and the indices
        are the information about time. The activity can be read with
        :func:`sksports.io.bikeread`.

    max_duration : Timedelta, timedelta, np.timedelta64, int, or str, optional
        The maximum duration for which the power-profile should be computed. By
        default, it will be computed for the duration of the activity. An
        integer represents seconds.

    Returns
    -------
    power_profile : Series
        A pandas Series containing the power-profile.

    References
    ----------
    .. [1] Pinot, J., and F. Grappe. "The record power profile to assess
       performance in elite cyclists." International journal of sports medicine
       32.11 (2011): 839-844.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.extraction import activity_power_profile
    >>> power_profile = activity_power_profile(bikeread(load_fit()[0]))
    >>> power_profile.head() # doctest : +NORMALIZE_WHITESPACE
    cadence  00:00:01    78.000000
             00:00:02    64.000000
             00:00:03    62.666667
             00:00:04    62.500000
             00:00:05    64.400000
    Name: 2014-05-07 12:26:22, dtype: float64

    """
    if max_duration is None:
        max_duration = pd.Timedelta(seconds=activity.shape[0])
    elif isinstance(max_duration, Integral):
        max_duration = pd.Timedelta(seconds=max_duration)
    else:
        max_duration = pd.Timedelta(max_duration)

    max_duration = min(
        max_duration,
        activity.index[-1] - activity.index[0] + pd.Timedelta(seconds=1))

    activity_power = activity['power']
    activity_complement = activity.drop(['power'], axis=1)

    # use the threading backend since we release the GIL.
    power_profile, power_profile_idx = zip(
        *[max_mean_power_interval(activity_power.values, duration)
          for duration in range(1, max_duration.seconds)])
    power_profile = np.array(power_profile)
    power_profile_idx = np.array(power_profile_idx)

    series_index = pd.timedelta_range(
        "00:00:01", timedelta(seconds=max_duration.seconds - 1), freq='s')
    series_name = pd.Timestamp(activity.index[0])

    # if some additional data are available, we will add them as them on the
    # side of the power-profile.
    if not activity_complement.empty:
        complement_data = {col: pd.Series(
            _associated_data_power_profile(activity_complement[col].values,
                                           power_profile_idx,
                                           np.arange(1, max_duration.seconds,
                                                     dtype=int)),
            index=series_index, name=series_name)
                           for col in activity_complement.columns}
        complement_data['power'] = pd.Series(power_profile, index=series_index,
                                             name=series_name)
        return pd.concat(complement_data)

    else:
        return pd.Series(power_profile, index=series_index, name=series_name)
