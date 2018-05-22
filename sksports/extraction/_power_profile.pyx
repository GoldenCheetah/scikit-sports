#cython: cdivision=True
#cython: boundscheck=False
#cython: nonecheck=False
#cython: wraparound=False

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from cython.parallel import parallel, prange
from libc.stdlib cimport malloc, free
cimport openmp
import numpy as np


cpdef (double, Py_ssize_t) max_mean_power_interval(
    floating[:] activity_power, Py_ssize_t time_interval) nogil:
    """Compute the maximum power delivered for a specific amount of time.

    Parameters
    ----------
    activity_power : ndarray, shape (n_samples,)
        The power data of the activity.

    time_interval : int
        The time interval for which we compute the mean power.

    Returns
    -------
    max_mean : double
        The maximum power delivered for a specific amount of time.

    """

    cdef:
        Py_ssize_t n_element = activity_power.shape[0]
        Py_ssize_t idx_element, idx_interval, idx_max_mean,
        double acc
        double* acc_arr = <double*>malloc((n_element - time_interval) *
                                           sizeof(double))
        # double[:] acc_arr = np.empty((n_element - time_interval,))
        Py_ssize_t idx_acc_arr
        double max_mean = 0.0

    with parallel():
        for idx_element in prange(n_element - time_interval):
            acc = 0.0
            for idx_interval in range(time_interval):
                acc = acc + activity_power[idx_element + idx_interval]
            acc_arr[idx_element] = acc
    for idx_acc_arr in range(n_element - time_interval):
        if acc_arr[idx_acc_arr] > max_mean:
            max_mean = acc_arr[idx_acc_arr]
            idx_max_mean = idx_acc_arr
    free(acc_arr)

    return max_mean / time_interval, idx_max_mean


cpdef _associated_data_power_profile(floating[:] data,
                                     integral[:] pp_index,
                                     integral[:] duration):
    """Compute the mean of the complementary data of the power-profile.

    Parameters
    ----------
    data : ndarray, shape (n_samples,)
        The complementary data to use.

    pp_index : ndarray, shape (max_duration,)
        The indices of the maximum for a specific duration found when computing
        the power-profile.

    duration : ndarray, shape (max_duration,)
        An array containing the duration (idx/integrer).

    Returns
    -------
    complement_data : ndarray, shape (max_duration)
        The mean of the complementary data of the power-profile for each
        duration.

    """
    cdef:
        Py_ssize_t time_interval, data_idx, i, j, n_elt
        double[:] output = np.empty((pp_index.shape[0],))
        double acc

    with nogil, parallel():
        for i in prange(pp_index.shape[0]):
            time_interval = duration[i]
            data_idx = pp_index[i]
            acc = 0.0
            for j from data_idx <= j < data_idx + time_interval:
                acc = acc + data[j]
            output[i] = acc / time_interval

    return np.array(output)
