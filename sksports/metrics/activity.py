# coding: utf-8

""" Metrics to asses the performance of a cycling ride.

Functions named as ``*_score`` return a scalar value to maximize: the higher
the better.

Function named as ``*_error`` or ``*_loss`` return a scalar value to minimize:
the lower the better.
"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from __future__ import division

import numpy as np

TS_SCALE_GRAPPE = dict([('I1', 2.), ('I2', 2.5), ('I3', 3.),
                        ('I4', 3.5), ('I5', 4.5), ('I6', 7.),
                        ('I7', 11.)])

ESIE_SCALE_GRAPPE = dict([('I1', (.3, .5)), ('I2', (.5, .6)),
                          ('I3', (.6, .75)), ('I4', (.75, .85)),
                          ('I5', (.85, 1.)), ('I6', (1., 1.80)),
                          ('I7', (1.8, 3.))])


def mpa2ftp(mpa):
    """Convert the maximum power aerobic into the functional threshold power.

    Parameters
    ----------
    mpa : float
        Maximum power aerobic.

    Return:
    -------
    ftp : float
        Functional threshold power.

    Examples
    --------
    >>> from sksports.metrics import mpa2ftp
    >>> print(mpa2ftp(400)) # doctest: +ELLIPSIS
    304...

    """
    return 0.76 * mpa


def ftp2mpa(ftp):
    """Convert the functional threshold power into the maximum threshold power.

    Parameters
    ----------
    ftp : float
        Functional threshold power.

    Return:
    -------
    mpa : float
        Maximum power aerobic.

    Examples
    --------
    >>> from sksports.metrics import ftp2mpa
    >>> print(ftp2mpa(304)) # doctest: +ELLIPSIS
    400...

    """
    return ftp / 0.76


def normalized_power_score(activity_power, mpa, window_width=30):
    """Normalized power®.

    The normalized power is an average power computing a smoothed power input
    and rejecting the low power intensities.

    Read more in the :ref:`User Guide <metrics>`.

    Parameters
    ----------
    activity_power : Series
        A Series containing the power data from an activity.

    mpa : float
        Maximum power aerobic. Use :func:`metrics.ftp2mpa` if you use the
        functional threshold power metric.


    window_width : int, optional
        The width of the window used to smooth the power data before to compute
        the normalized power. The default width is 30 samples.

    Returns
    -------
    score : float
        Normalized power score.

    References
    ----------
    .. [1] Allen, H., and A. Coggan. "Training and racing with a power
       meter." VeloPress, 2012.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.metrics import normalized_power_score
    >>> ride = bikeread(load_fit()[0])
    >>> mpa = 400
    >>> np = normalized_power_score(ride['power'], mpa)
    >>> print('Normalized power {:.2f} W'.format(np))
    Normalized power 218.49 W

    """

    smooth_activity = (activity_power.rolling(window_width, center=True)
                                     .mean().dropna())
    # removing value < I1-ESIE, i.e. 30 % MPA
    smooth_activity = smooth_activity[
        smooth_activity > ESIE_SCALE_GRAPPE['I1'][0] * mpa]

    return (smooth_activity ** 4).mean() ** (1 / 4)


def intensity_factor_score(activity_power, mpa):
    """Intensity factor®.

    The intensity factor® is the ratio of the normalized power® over the
    functional threshold power. Note that all our computation consider the
    maximum power aerobic for consistency. If you only have the functional
    threshold power, use :func:`metrics.ftp2mpa`.

    Read more in the :ref:`User Guide <metrics>`.

    Parameters
    ----------
    activity_power : Series
        A Series containing the power data from an activity.

    mpa : float
        Maximum power aerobic. Use :func:`metrics.ftp2mpa` if you use the
        functional threshold power metric.

    Returns
    -------
    score: float
        Intensity factor.

    References
    ----------
    .. [1] Allen, H., and A. Coggan. "Training and racing with a power
       meter." VeloPress, 2012.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.metrics import intensity_factor_score
    >>> ride = bikeread(load_fit()[0])
    >>> mpa = 400
    >>> if_score = intensity_factor_score(ride['power'], mpa)
    >>> print('Intensity factor {:.2f} W'.format(if_score))
    Intensity factor 0.72 W

    """
    ftp = mpa2ftp(mpa)
    return normalized_power_score(activity_power, mpa) / ftp


def training_stress_score(activity_power, mpa):
    """Training stress score®.

    The training stress score® corresponds to the intensity factor® normalized
    by the time of the activity. You can use the function
    :func:`metrics.ftp2mpa` if you are using the functional threshold metric.

    Read more in the :ref:`User Guide <metrics>`.

    Parameters
    ----------
    activity_power : Series
        A Series containing the power data from an activity.

    mpa : float
        Maximum power aerobic. Use :func:`metrics.ftp2mpa` if you use the
        functional threshold power metric.

    Returns
    -------
    score: float
        Training stress score.

    References
    ----------
    .. [1] Allen, H., and A. Coggan. "Training and racing with a power
       meter." VeloPress, 2012.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.metrics import training_stress_score
    >>> ride = bikeread(load_fit()[0])
    >>> mpa = 400
    >>> ts_score = training_stress_score(ride['power'], mpa)
    >>> print('Training stress score {:.2f}'.format(ts_score))
    Training stress score 32.38

    """
    activity_power = activity_power.resample('1S').mean()
    if_score = intensity_factor_score(activity_power, mpa)
    return (activity_power.size * if_score ** 2) / 3600 * 100


def training_load_score(activity_power, mpa):
    """Training load score.

    Grappe et al. proposes to compute the load of an activity by a weighted sum
    of the time spend in the different ESIE zones.

    Read more in the :ref:`User Guide <metrics>`.

    Parameters
    ----------
    activity_power : Series
        A Series containing the power data from an activity.

    mpa : float
        Maximum power aerobic. Use :func:`metrics.ftp2mpa` if you use the
        functional threshold power metric.

    Returns
    -------
    tls_score: float
        Training load score.

    References
    ----------
    .. [1] Grappe, F. "Cyclisme et optimisation de la performance: science
       et méthodologie de l'entraînement." De Boeck Supérieur, 2009.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> from sksports.io import bikeread
    >>> from sksports.metrics import training_load_score
    >>> ride = bikeread(load_fit()[0])
    >>> mpa = 400
    >>> tl_score = training_load_score(ride['power'], mpa)
    >>> print('Training load score {:.2f}'.format(tl_score))
    Training load score 74.90

    """
    tls_score = 0.
    activity_power = activity_power.resample('1S').mean()
    for key in TS_SCALE_GRAPPE.keys():
        power_samples = activity_power[
            np.bitwise_and(activity_power >= ESIE_SCALE_GRAPPE[key][0] * mpa,
                           activity_power < ESIE_SCALE_GRAPPE[key][1] * mpa)]
        tls_score += power_samples.size / 60 * TS_SCALE_GRAPPE[key]
    return tls_score
