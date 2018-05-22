# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from os.path import join

import pytest

from sksports.datasets import load_fit
from sksports.datasets import load_rider


@pytest.mark.parametrize(
    "returned_type, set_data, expected_filenames",
    [('list_file', 'normal', sorted(['2014-05-11-11-39-38.fit',
                                     '2014-05-07-14-26-22.fit',
                                     '2014-07-26-18-50-56.fit'])),
     ('path', 'normal', ['data']),
     ('list_file', 'corrupted', sorted(['2013-04-24-22-22-25.fit',
                                        '2014-05-17-10-44-53.fit',
                                        '2015-11-27-18-54-57.fit'])),
     ('path', 'corrupted', ['corrupted_data'])])
def test_load_fit(returned_type, set_data, expected_filenames):
    filenames = load_fit(returned_type=returned_type,
                         set_data=set_data)
    if not isinstance(filenames, list):
        filenames = [filenames]
    for f, e in zip(filenames, expected_filenames):
        assert e in f


def test_load_rider():
    filename = load_rider()
    assert join('data', 'rider.csv') in filename
