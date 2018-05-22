"""
The :mod:`sksports.extraction` module includes algorithms to extract
information from cycling data.
"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from .gradient import acceleration
from .gradient import gradient_activity
from .gradient import gradient_elevation
from .gradient import gradient_heart_rate

from .power_profile import activity_power_profile


__all__ = ['acceleration',
           'gradient_activity',
           'gradient_elevation',
           'gradient_heart_rate',
           'activity_power_profile']
