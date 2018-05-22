# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from cython cimport floating, integral


cpdef (double, Py_ssize_t) max_mean_power_interval(
    floating[:] activity_power, Py_ssize_t time_interval) nogil


cpdef _associated_data_power_profile(floating[:] data,
                                     integral[:] pp_index,
                                     integral[:] duration)
