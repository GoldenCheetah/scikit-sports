"""Function to extract gradient information about different features."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from __future__ import division

from collections import Iterable

import pandas as pd

from ..exceptions import MissingDataError


def acceleration(activity, periods=5, append=True):
    """Compute the acceleration (i.e. speed gradient).

    Read more in the :ref:`User Guide <gradient>`.

    Parameters
    ----------
    activity : DataFrame
        The activity containing speed information.

    periods : int, default=5
        Periods to shift to compute the acceleration.

    append : bool, optional
        Whether to append the acceleration to the original activity (default)
        or to only return the acceleration as a Series.

    Returns
    -------
    data : DataFrame or Series
        The original activity with an additional column containing the
        acceleration or a single Series containing the acceleration.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.extraction import acceleration
    >>> ride = bikeread(load_fit()[0])
    >>> new_ride = acceleration(ride)

    """
    if 'speed' not in activity.columns:
        raise MissingDataError('To compute the acceleration, speed data are '
                               'required. Got {} fields.'
                               .format(activity.columns))

    acceleration = activity['speed'].diff(periods=periods) / periods

    if append:
        activity['acceleration'] = acceleration
        return activity
    else:
        return acceleration


def gradient_elevation(activity, periods=5, append=True):
    """Compute the elevation gradient.

    Read more in the :ref:`User Guide <gradient>`.

    Parameters
    ----------
    activity : DataFrame
        The activity containing elevation and distance information.

    periods : int, default=5
        Periods to shift to compute the elevation gradient.

    append : bool, optional
        Whether to append the elevation gradient to the original activity
        (default) or to only return the elevation gradient as a Series.

    Returns
    -------
    data : DataFrame or Series
        The original activity with an additional column containing the
        elevation gradient or a single Series containing the elevation
        gradient.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.extraction import gradient_elevation
    >>> ride = bikeread(load_fit()[0])
    >>> new_ride = gradient_elevation(ride)

    """
    if not {'elevation', 'distance'}.issubset(activity.columns):
        raise MissingDataError('To compute the elevation gradient, elevation '
                               'and distance data are required. Got {} fields.'
                               .format(activity.columns))

    diff_elevation = activity['elevation'].diff(periods=periods)
    diff_distance = activity['distance'].diff(periods=periods)
    gradient_elevation = diff_elevation / diff_distance

    if append:
        activity['gradient-elevation'] = gradient_elevation
        return activity
    else:
        return gradient_elevation


def gradient_heart_rate(activity, periods=5, append=True):
    """Compute the heart-rate gradient.

    Read more in the :ref:`User Guide <gradient>`.

    Parameters
    ----------
    activity : DataFrame
        The activity containing heart-rate information.

    periods : int, default=5
        Periods to shift to compute the heart-rate gradient.

    append : bool, optional
        Whether to append the heart-rate gradient to the original activity
        (default) or to only return the heart-rate gradient as a Series.

    Returns
    -------
    data : DataFrame or Series
        The original activity with an additional column containing the
        heart-rate gradient or a single Series containing the heart-rate
        gradient.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.extraction import gradient_heart_rate
    >>> ride = bikeread(load_fit()[0])
    >>> ride['heart-rate'] = pd.Series(
    ...     np.random.randint(60, 200, size=ride.shape[0]),
    ...     index=ride.index)  # Add fake heart-rate data for the example
    >>> new_ride = gradient_heart_rate(ride)

    """
    if 'heart-rate' not in activity.columns:
        raise MissingDataError('To compute the heart-rate gradient, heart-rate'
                               ' data are required. Got {} fields.'
                               .format(activity.columns))

    gradient_heart_rate = activity['heart-rate'].diff(periods=periods)

    if append:
        activity['gradient-heart-rate'] = gradient_heart_rate
        return activity
    else:
        return gradient_heart_rate


def gradient_activity(activity, periods=1, append=True, columns=None):
    """Compute the gradient for all given columns.

    Read more in the :ref:`User Guide <gradient>`.

    Parameters
    ----------
    activity : DataFrame
        The activity to use to compute the gradient.

    periods : int or array-like, default=1
        Periods to shift to compute the gradient. If an array-like is given,
        several gradient will be computed.

    append : bool, optional
        Whether to append the gradients to the original activity.

    columns : list, optional
        The name of the columns to use to compute the gradient. By default, all
        the columns are used.

    Returns
    -------
    gradient : DataFrame
        The computed gradient from the activity.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.extraction import gradient_activity
    >>> ride = bikeread(load_fit()[0], drop_nan='columns')
    >>> new_ride = acceleration(ride)

    """
    if columns is not None:
        data = activity[columns]
    else:
        data = activity

    if isinstance(periods, Iterable):
        gradient = [data.diff(periods=p) for p in periods]
        gradient_name = ['gradient_{}'.format(p) for p in periods]
    else:
        gradient = [data.diff(periods=periods)]
        gradient_name = ['gradient_{}'.format(periods)]

    if append:
        # prepend the original information
        gradient = [activity] + gradient
        gradient_name = ['original'] + gradient_name

    return pd.concat(gradient, axis=1, keys=gradient_name)
