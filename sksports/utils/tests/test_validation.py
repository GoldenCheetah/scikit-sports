# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

from os.path import dirname, join

import pytest

from sksports.datasets import load_fit
from sksports.utils import validate_filenames

filenames = load_fit()


@pytest.mark.parametrize(
    "filenames, expected_filenames",
    [(filenames, filenames),
     (join(dirname(filenames[0]), '*.fit'), filenames)])
def test_validate_filenames(filenames, expected_filenames):
    assert list(validate_filenames(filenames)) == expected_filenames
