.. _utilities:

.. currentmodule:: sksports

=========
Utilities
=========

.. _gradient:

Extract additional information from activities
----------------------------------------------

The :mod:`extraction` allows to extract supplement information from the
original data read using the :func:`io.bikeread`.

The acceleration is computed from the speed using the function
:func:`extraction.acceleration`::

   >>> from sksports.datasets import load_fit
   >>> from sksports.io import bikeread
   >>> from sksports.extraction import acceleration
   >>> ride = bikeread(load_fit()[0])
   >>> new_ride = acceleration(ride)

In a similar manner this is possible to compute the grade of a slope using the
function :func:`extraction.gradient_elevation`::

  >>> from sksports.datasets import load_fit
  >>> from sksports.io import bikeread
  >>> from sksports.extraction import gradient_elevation
  >>> ride = bikeread(load_fit()[0])
  >>> new_ride = gradient_elevation(ride)

The gradient of the heart-rate is computed using the function
:func:`extraction.gradient_heart_rate`::

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

Note that for this example, we created some fake data since the original data
do not have any heart-rate information.

Finally, you can compute the gradient of any field present in the DataFrame
using the function `extraction.gradient_activity`::

  >>> from sksports.datasets import load_fit
  >>> from sksports.io import bikeread
  >>> from sksports.extraction import gradient_activity
  >>> ride = bikeread(load_fit()[0], drop_nan='columns')
  >>> new_ride = acceleration(ride)

All those methods have a ``periods`` argument which specify between which data
points the gradient will be computed.
