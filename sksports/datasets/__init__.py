"""
The :mod:`sksports.datasets` module includes utilities to load datasets.
"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from os import listdir
from os.path import dirname, join

__all__ = ['load_fit',
           'load_rider']


def load_fit(returned_type='list_file', set_data='normal'):
    """Return path to some FIT toy data.

    Read more in the :ref:`User Guide <datasets>`.

    Parameters
    ----------
    returned_type : str, optional (default='list_file')
        If 'list_file', return a list containing the fit files;
        If 'path', return a string where the data are localized.

    set_data : str, optional (default='normal')
        If 'normal', return 3 files.
        If 'corrupted, return corrupted files for testing.

    Returns
    -------
    filenames : str or list of str,
        List of string or string depending of input parameters.

    Examples
    --------
    >>> from sksports.datasets import load_fit
    >>> load_fit() # doctest : +ELLIPSIS
    [...]

    """
    module_path = dirname(__file__)

    if set_data == 'normal':
        if returned_type == 'list_file':
            return sorted([
                join(module_path, 'data', name)
                for name in listdir(join(module_path, 'data'))
                if name.endswith('.fit')
            ])
        elif returned_type == 'path':
            return join(module_path, 'data')
    elif set_data == 'corrupted':
        if returned_type == 'list_file':
            return sorted([
                join(module_path, 'corrupted_data', name)
                for name in listdir(
                    join(module_path, 'corrupted_data'))
                if name.endswith('.fit')
            ])
        elif returned_type == 'path':
            return join(module_path, 'corrupted_data')


def load_rider():
    """Return the path to a CSV file containing rider information.

    Read more in the :ref:`User Guide <datasets>`.

    Parameters
    ----------
    None

    Returns
    -------
    filename : str
        The path to the CSV file.

    Examples
    --------
    >>> from sksports.datasets import load_rider
    >>> load_rider() # doctest : +ELLIPSIS
    '...rider.csv'

    """
    module_path = dirname(__file__)

    return join(module_path, 'data', 'rider.csv')
