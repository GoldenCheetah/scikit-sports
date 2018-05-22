"""Methods to load power data file."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import numpy as np

from .fit import load_power_from_fit

DROP_OPTIONS = ('columns', 'rows', 'both')


def bikeread(filename, drop_nan=None):
    """Read power data file.

    Read more in the :ref:`User Guide <reader>`.

    Parameters
    ----------
    filename : str
        Path to the file to read.

    drop_nan : str {'columns', 'rows', 'both'} or None
        Either to remove the columns/rows containing NaN values. By default,
        all data will be kept.

    Returns
    -------
    data : DataFrame
        Power data and time data.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> activity = bikeread(load_fit()[0], drop_nan='columns')
    >>> activity.head() # doctest : +NORMALIZE_WHITESPACE
                         elevation  cadence  distance  power  speed
    2014-05-07 12:26:22       64.8     45.0      3.05  256.0  3.036
    2014-05-07 12:26:23       64.8     42.0      6.09  185.0  3.053
    2014-05-07 12:26:24       64.8     44.0      9.09  343.0  3.004
    2014-05-07 12:26:25       64.8     45.0     11.94  344.0  2.846
    2014-05-07 12:26:26       65.8     48.0     15.03  389.0  3.088

    """
    if drop_nan is not None and drop_nan not in DROP_OPTIONS:
        raise ValueError('"drop_nan" should be one of {}.'
                         ' Got {} instead.'.format(DROP_OPTIONS, drop_nan))

    df = load_power_from_fit(filename)

    if drop_nan is not None:
        if drop_nan == 'columns':
            df.dropna(axis=1, inplace=True)
        elif drop_nan == 'rows':
            df.dropna(axis=0, inplace=True)
        else:
            df.dropna(axis=1, inplace=True).dropna(axis=0, inplace=True)

    # remove possible outliers by clipping the value
    df[df['power'] > 2500.] = np.nan

    # resample to have a precision of a second with additional linear
    # interpolation for missing value
    return df.resample('s').interpolate('linear')
