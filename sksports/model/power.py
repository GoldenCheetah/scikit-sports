"""Module to estimate power from data."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from __future__ import division

import numpy as np
from scipy import constants

from ..extraction import gradient_elevation
from ..extraction import acceleration


def strava_power_model(activity, cyclist_weight, bike_weight=6.8,
                       coef_roll_res=0.0045, pressure=101325.0,
                       temperature=15.0, coef_drag=1, surface_rider=0.32,
                       use_acceleration=False):
    """Strava model used to estimate power.

    It corresponds the mathematical formulation which add all forces applied to
    a cyclist in movement.

    Read more in the :ref:`User Guide <strava>`.

    Parameters
    ----------
    activity : DataFrame
        The activity containing the ride information.

    cyclist_weight : float
        The cyclist weight in kg.

    bike_weight : float, default=6.8
        The bike weight in kg.

    coef_roll_res : float, default=0.0045
        Rolling resistance coefficient.

    pressure : float, default=101325.0
        Pressure in Pascal.

    temperature : float, default=15.0
        Temperature in Celsius.

    coef_drag : float, default=1
        The drag coefficient also known as Cx.

    surface_rider : float, default=0.32
        Surface area of the rider facing wind also known as S. The unit is m^2.

    use_acceleration : bool, default=False
        Either to add the power required to accelerate. This estimation can
        become unstable if the acceleration varies for reason which are not
        linked to power changes (i.e., braking, bends, etc.)

    Returns
    -------
    power : Series
        The power estimated.

    References
    ----------
    .. [1] How Strava Calculates Power
       https://support.strava.com/hc/en-us/articles/216917107-How-Strava-Calculates-Power

    Examples
    --------
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

    """
    if 'gradient-elevation' not in activity.columns:
        activity = gradient_elevation(activity)
    if use_acceleration and 'acceleration' not in activity.columns:
        activity = acceleration(activity)

    temperature_kelvin = constants.convert_temperature(
        temperature, 'Celsius', 'Kelvin')
    total_weight = cyclist_weight + bike_weight  # kg

    speed = activity['speed']  # m.s^-1
    power_roll_res = coef_roll_res * constants.g * total_weight * speed

    # air density at 0 degree Celsius and a standard atmosphere
    molar_mass_dry_air = 28.97 / 1000  # kg.mol^-1
    standard_atmosphere = constants.physical_constants[
        'standard atmosphere'][0]  # Pa
    zero_celsius_kelvin = constants.convert_temperature(
        0, 'Celsius', 'Kelvin')  # 273.15 K
    air_density_ref = (
        (standard_atmosphere * molar_mass_dry_air) /
        (constants.gas_constant * zero_celsius_kelvin))  # kg.m^-3
    air_density = air_density_ref * (
        (pressure * zero_celsius_kelvin) /
        (standard_atmosphere * temperature_kelvin))  # kg.m^-3
    power_wind = 0.5 * air_density * surface_rider * coef_drag * speed**3

    slope = activity['gradient-elevation']  # grade
    power_gravity = (total_weight * constants.g *
                     np.sin(np.arctan(slope)) * speed)

    power_total = power_roll_res + power_wind + power_gravity

    if use_acceleration:
        acc = activity['acceleration']  # m.s^-1
        power_acceleration = total_weight * acc
        # multiply by the average speed between t and t-1
        power_acceleration = power_acceleration * (speed * (1 + acc)) / 2
        power_total = power_total + power_acceleration

    return power_total.clip(0)
