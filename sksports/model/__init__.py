"""
The :mod:`sksports.model` module includes algorithms to model cycling data.
"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from .power import strava_power_model

__all__ = ['strava_power_model']
