"""Methods to handle input/output files."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import os
from collections import defaultdict

import pandas as pd
import numpy as np
import six

from fitparse import FitFile

# 'timestamp' will be consider as the index of the DataFrame later on
FIELDS_DATA = ('timestamp', 'power', 'heart_rate', 'cadence', 'distance',
               'altitude', 'speed')


def check_filename_fit(filename):
    """Method to check if the filename corresponds to a fit file.

    Parameters
    ----------
    filename : str
        The fit file to check.

    Returns
    -------
    filename : str
        The checked filename.

    """

    # Check that filename is of string type
    if isinstance(filename, six.string_types):
        # Check that this is a fit file
        if filename.endswith('.fit'):
            # Check that the file is existing
            if os.path.isfile(filename):
                return filename
            else:
                raise ValueError('The file does not exist.')
        else:
            raise ValueError('The file is not a fit file.')
    else:
        raise ValueError('filename needs to be a string. Got {}'.format(
            type(filename)))


def load_power_from_fit(filename):
    """Method to open the power data from FIT file into a pandas dataframe.

    Parameters
    ----------
    filename : str,
        Path to the FIT file.

    Returns
    -------
    data : DataFrame
        Power records of the ride.

    """
    filename = check_filename_fit(filename)
    activity = FitFile(filename)
    activity.parse()
    records = activity.get_messages(name='record')

    data = defaultdict(list)
    for rec in records:
        values = rec.get_values()
        for key in FIELDS_DATA:
            data[key].append(values.get(key, np.NaN))

    data = pd.DataFrame(data)
    if data.empty:
        raise IOError('The file {} does not contain any data.'.format(
            filename))

    # rename the columns for consistency
    data.rename(columns={'heart_rate': 'heart-rate', 'altitude': 'elevation'},
                inplace=True)

    data.set_index(FIELDS_DATA[0], inplace=True)
    del data.index.name

    return data
