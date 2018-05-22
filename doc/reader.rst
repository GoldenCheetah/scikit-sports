.. _reader:

.. currentmodule:: sksports

==========================
Input/Output Cycling Files
==========================

The :mod:`io` allows to manipulate cycling files acquired with different
devices. :func:`io.bikeread` is the centralized interface to open any file
format::

  >>> from sksports.datasets import load_fit
  >>> from sksports.io import bikeread
  >>> ride = bikeread(load_fit()[0])
  >>> print(ride.head())
                       elevation  cadence  distance  heart-rate  power  speed
  2014-05-07 12:26:22       64.8     45.0      3.05         NaN  256.0  3.036
  2014-05-07 12:26:23       64.8     42.0      6.09         NaN  185.0  3.053
  2014-05-07 12:26:24       64.8     44.0      9.09         NaN  343.0  3.004
  2014-05-07 12:26:25       64.8     45.0     11.94         NaN  344.0  2.846
  2014-05-07 12:26:26       65.8     48.0     15.03         NaN  389.0  3.088

:func:`io.bikeread` returns a pandas DataFrame with the index containing the
date and time of the activity while the columns contain the following data:

* elevation;
* cadence;
* distance;
* heart-rate;
* power;
* speed.

If some of those data are not available, the corresponding column will contain
``NaN`` values by default. ``drop_nan`` argument allows to drop columns or rows
containing missing data::

  >>> ride = bikeread(load_fit()[0], drop_nan='columns')
  >>> print(ride.head())
                       elevation  cadence  distance  power  speed
  2014-05-07 12:26:22       64.8     45.0      3.05  256.0  3.036
  2014-05-07 12:26:23       64.8     42.0      6.09  185.0  3.053
  2014-05-07 12:26:24       64.8     44.0      9.09  343.0  3.004
  2014-05-07 12:26:25       64.8     45.0     11.94  344.0  2.846
  2014-05-07 12:26:26       65.8     48.0     15.03  389.0  3.088


.. topic:: Examples:

    * :ref:`sphx_glr_auto_examples_input_output_plot_bikeread_usage.py`
    * :ref:`sphx_glr_auto_examples_input_output_plot_activity_data.py`
