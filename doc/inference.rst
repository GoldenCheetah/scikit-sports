.. _inference:

.. currentmodule:: sksports

=========
Inference
=========

Power inference
---------------

Power meters are expensive tools and it is possible to get an estimate using
simple data which are acquired through phone or GPS-based cycling computer. We
are presenting several models which allow to estimate the power from those
data.

.. _strava:

Physical model using all forces applied to a cyclist
....................................................

This is possible to compute the power by adding all forces applied to cyclist
in motion. The mathematical formulation of such model is:

.. math::
   P_{meca} = \left( \frac{1}{2} \rho \cdot SC_x \cdot V_a^2 + C_r \cdot mg \cdot \cos \alpha + mg \cdot \sin \alpha + m \cdot a \right) \cdot V_d

where :math:`\rho` is the air density in :math:`kg.m^{-3}`, :math:`S` is
frontal surface of the cyclist in :math:`m^2`, :math:`C_x` is the drag
coefficient, :math:`V_a` is the air speed in :math:`m.s^{-1}`, :math:`C_r` is
the rolling coefficient, :math:`m` is the mass of the rider and bicycle in
:math:`kg`, :math:`g` in the gravitational constant which is equal to 9.81
:math:`m.s^{-2}`, :math:`\alpha` is the slope in radian, :math:`a` is the
acceleration in :math:`m.s^{-1}`, and :math:`V_d` is the rider speed in
:math:`m.s^{-1}`.

The function :func:`model.strava_power_model` allows to estimate the power
using this model. Note that we are using the default argument but the you can
set more precisely the argument to fit your condition. To estimate, we need
to::

  >>> from sksports.datasets import load_fit
  >>> from sksports.io import bikeread
  >>> from sksports.model import strava_power_model
  >>> ride = bikeread(load_fit()[0])
  >>> power = strava_power_model(ride, cyclist_weight=72)
  >>> print(power['2014-05-07 12:26:28':
  ...             '2014-05-07 12:26:38'])  # Show 10 sec of estimated power
  2014-05-07 12:26:28    196.567898
  2014-05-07 12:26:29    198.638094
  2014-05-07 12:26:30    191.444894
  2014-05-07 12:26:31     26.365864
  2014-05-07 12:26:32     89.826104
  2014-05-07 12:26:33    150.842325
  2014-05-07 12:26:34    210.083958
  2014-05-07 12:26:35    331.573965
  2014-05-07 12:26:36    425.013711
  2014-05-07 12:26:37    428.806914
  2014-05-07 12:26:38    425.410451
  Freq: S, dtype: float64

By default the term :math:`g \cdot a \cdot V_d` is not computed. Using this
term, the results can be unstable when the change of power is non smooth. To
enable it, turn ``use_acceleration=True``

.. topic:: Examples:

    * :ref:`sphx_glr_auto_examples_model_plot_physic_model.py`


.. _machine_learning:

Machine learning model
......................

This part is in progress. Find more at
`this link <https://github.com/scikit-sports/research/tree/master/power_regression>`_.
