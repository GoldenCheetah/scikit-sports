""" Metrics to asses the power profile. """

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from __future__ import division

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression


SAMPLING_WKO = pd.TimedeltaIndex(
    ['00:00:01', '00:00:05', '00:00:30', '00:01:00', '00:03:00',
     '00:03:30', '00:04:00', '00:04:30', '00:05:00', '00:05:30',
     '00:06:00', '00:06:30', '00:07:00', '00:10:00', '00:20:00',
     '00:30:00', '00:45:00', '01:00:00', '02:00:00', '03:00:00',
     '04:00:00'])


def std_dev_squared_error(y_true, y_pred):
    """Compute the standard deviation of the squared error.

    Parameters
    ----------
    y_true : ndarray, shape (n_samples,)
        Ground truth (correct) target values.

    y_pred : ndarray, shape (n_samples,)
        Estimated target values.

    Returns
    -------
    std_dev : float
        Standard deviation of the squared error.

    """

    return np.sqrt(np.sum((y_true - y_pred) ** 2 / (y_true.size - 2)))


def aerobic_meta_model(record_power_profile, time_samples=None):
    """Compute the aerobic metabolism model from the record power-profile.

    Read more in the :ref:`User Guide <mpa_estimate>`.

    Parameters
    ----------
    record_power_profile : Series
        The record power profile from which to extract the aerobic model.

    time_samples : TimedeltaIndex or None, optional
        The time samples of the record power-profile to take into account. If
        None, the sampling of the method of Pinot et al. is applied, which is
        equivalent to the sampling from WKO+.

    Returns
    -------
    mpa : float
        Maximum Aerobic Power.

    t_mpa : Timedelta
        Time of the Maximum Aerobic Power.

    aei : float
        Aerobic Endurance Index.

    fit_info_mpa_fitting : dict
        This is a dictionary with the information collected about the fitting
        related to the MAP. The attributes will be the following:

        - `slope`: slope of the linear fitting,
        - `intercept`: intercept of the linear fitting,
        - `std_err`: standard error of the fitting,
        - `coeff_det`: coefficient of determination.

    fit_info_aei_fitting : dict
        This is a dictionary with the information collected about the fitting
        related to the AEI. The attributes will be the following:

        - `slope`: slope of the linear fitting,
        - `intercept`: intercept of the linear fitting,
        - `std_err`: standard error of the fitting,
        - `coeff_det`: coefficient of determination.

    Notes
    -----
    The method implemented here follow the work presented in [1]_.

    References
    ----------
    .. [1] Pinot et al., "Determination of Maximal Aerobic Power
       on the Field in Cycling", Jounal of Science and Cycling, vol. 3(1),
       pp. 26-31, 2014.

    """
    if time_samples is None:
        time_samples = SAMPLING_WKO.copy()

    # keep only the time samples available in the record power-profile
    mask_time_samples = time_samples < record_power_profile.index.max()
    time_samples = time_samples[mask_time_samples]

    # to avoid losing data, we will first interpolate the time samples
    # using all the data available in the record power-profile before
    # to select only the samples required.
    ts_union = record_power_profile.index.union(time_samples)
    record_power_profile = (record_power_profile.reindex(ts_union)
                                                .interpolate('linear')
                                                .reindex(time_samples))

    # only samples between 10 minutes and 4 hours are considered for the
    # regression
    mask_samples_map = np.bitwise_and(time_samples >= '00:10:00',
                                      time_samples <= '04:00:00')
    extracted_profile = record_power_profile.loc[mask_samples_map].values
    extracted_time = record_power_profile.loc[mask_samples_map].index.values
    extracted_time = np.log(extracted_time /
                            np.timedelta64(1, 's')).reshape(-1, 1)

    ols = LinearRegression()
    ols.fit(extracted_time, extracted_profile)
    std_fit = std_dev_squared_error(extracted_profile,
                                    ols.predict(extracted_time))

    fit_info_mpa_fitting = {
        'slope': ols.coef_[0],
        'intercept': ols.intercept_,
        'std_err': std_fit,
        'coeff_det': ols.score(extracted_time, extracted_profile)}

    # mpa will be find between 3 minutes and 7 minutes
    mask_samples_map = np.bitwise_and(time_samples >= '00:03:00',
                                      time_samples <= '00:10:00')
    extracted_profile = record_power_profile.loc[mask_samples_map].values
    extracted_time = record_power_profile.loc[mask_samples_map].index.values
    extracted_time = np.log(extracted_time /
                            np.timedelta64(1, 's')).reshape(-1, 1)
    aerobic_model = ols.predict(extracted_time)

    # find the first value in the 2 * std confidence interval
    samples_within = np.abs(extracted_profile - aerobic_model) < 2 * std_fit

    if np.count_nonzero(samples_within):
        index_mpa = np.flatnonzero(samples_within)[0]
        time_mpa = record_power_profile.loc[mask_samples_map].index[index_mpa]
        mpa = record_power_profile.loc[mask_samples_map].iloc[index_mpa]
    else:
        raise ValueError('There is no value entering in the confidence'
                         ' level between 3 and 7 minutes.')

    # find aerobic endurance index
    mask_samples_aei = np.bitwise_and(time_samples >= time_mpa,
                                      time_samples <= '04:00:00')
    extracted_profile = record_power_profile.loc[mask_samples_aei].values
    extracted_profile = extracted_profile / mpa * 100
    extracted_time = record_power_profile.loc[mask_samples_aei].index.values
    extracted_time = np.log(extracted_time /
                            np.timedelta64(1, 's')).reshape(-1, 1)

    ols.fit(extracted_time, extracted_profile)
    fit_info_aei_fitting = {
        'slope': ols.coef_[0],
        'intercept': ols.intercept_,
        'std_err': std_fit,
        'coeff_det': ols.score(extracted_time, extracted_profile)}

    return (mpa, time_mpa, ols.coef_[0],
            fit_info_mpa_fitting, fit_info_aei_fitting)
