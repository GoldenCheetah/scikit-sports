"""Module containing the exceptions used in scikit-sports."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

__all__ = ['MissingDataError']


class MissingDataError(ValueError):
    """Error raised when there is not the required data to make some
    computation.

    For instance, :func:`sksports.extraction.gradient_elevation` required
    elevation and distance data which might not be provided. In this case, this
    type of error is raised.

    """
