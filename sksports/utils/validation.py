"""Utilities for input validation."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import glob
import os
from itertools import chain


def validate_filenames(filenames):
    """Check the filenames and expand in the case of wildcard.

    Parameters
    ----------
    filenames : str or list of str

        The path to the file to read. The input accepted are:

        * a filename or a list of filename to the file to read;
        * a filename or a list of filename containing a wildcard
          (e.g. ``'./data/*.fit'``).

    Returns
    -------
    filenames : list of str
        Returns a list of all file names.

    Examples
    --------
    >>> from sksports.utils import validate_filenames
    >>> from sksports.datasets import load_fit
    >>> filenames = validate_filenames(load_fit())
    >>> list(filenames) # doctest : +ELLIPSIS
    [...]

    """
    if isinstance(filenames, list):
        return chain.from_iterable([sorted(glob.glob(os.path.expanduser(f)))
                                    for f in filenames])
    else:
        return sorted(glob.glob(os.path.expanduser(filenames)))
