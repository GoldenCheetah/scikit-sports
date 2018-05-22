""" Testing the input/output methods for FIT files """

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import pytest

import numpy as np

from datetime import date

from numpy.testing import assert_allclose

from sksports.datasets import load_fit
from sksports.io.fit import load_power_from_fit
from sksports.io.fit import check_filename_fit


ride = np.array(
    [
        120, 123, 120, 120, 124, 124, 121, 132, 40, 71, 174, 196, 224, 165,
        148, 194, 176, 175, 201, 245, 218, 234, 240, 207, 233, 218, 266, 246,
        291, 281, 290, 236, 207, 132, 104, 95, 79, 141, 238, 252, 211, 250,
        201, 219, 177, 180, 202, 199, 210, 213, 201, 217, 211, 172, 213, 213,
        177, 216, 205, 174, 208, 200, 206, 202, 189, 205, 186, 207, 195, 204,
        207, 206, 191, 208, 208, 201, 209, 203, 219, 194, 200, 203, 199, 196,
        213, 198, 198, 198, 201, 202, 206, 202, 204, 209, 203, 196, 207, 205,
        209, 210, 202, 195, 199, 199, 204, 205, 199, 196, 195, 192, 207, 198,
        184, 207, 198, 210, 193, 204, 193, 182, 194, 174, 186, 188, 195, 182,
        228, 246, 236, 239, 238, 262, 240, 242, 236, 246, 244, 253, 247, 269,
        280, 248, 256, 243, 225, 307, 243, 258, 286, 218, 260, 262, 243, 253,
        251, 256, 249, 259, 257, 239, 246, 241, 249, 235, 243, 253, 245, 322,
        270, 320, 299, 278, 244, 295, 230, 271, 289, 266, 251, 250, 290, 281,
        262, 270, 266, 279, 264, 277, 275, 291, 282, 272, 258, 258, 294, 275,
        269, 267, 266, 276, 280, 296, 280, 362, 300, 313, 337, 304, 295, 305,
        331, 286, 289, 325, 289, 280, 341, 328, 328, 302, 302, 353, 305, 290,
        318, 308, 293, 285, 253, 243, 351, 388, 374, 363, 374, 319, 319, 348,
        342, 344, 347, 362, 371, 365, 335, 340, 356, 337, 327, 335, 309, 360,
        378, 395, 360, 325, 379, 370, 215, 0, 12, 19, 20, 17, 15, 3, 0, 0
    ],
    dtype=float)


@pytest.mark.parametrize(
    "filename",
    [('example.txt'),
     ('example.fit')])
def test_load_power_error(filename):
    with pytest.raises(ValueError):
        load_power_from_fit(filename)


def test_load_power_if_no_record():
    filenames = load_fit(set_data='corrupted')
    pattern = '2015-11-27-18-54-57.fit'
    for f in filenames:
        if pattern in f:
            filename = f
    msg = "does not contain any data."
    with pytest.raises(IOError, message=msg):
        load_power_from_fit(filename)


def test_load_power_normal_file():
    filenames = load_fit(set_data='corrupted')
    pattern = '2013-04-24-22-22-25.fit'
    for f in filenames:
        if pattern in f:
            filename = f
    df = load_power_from_fit(filename)
    assert_allclose(df['power'], ride)
    assert df.index[0].date() == date(2013, 4, 24)


@pytest.mark.parametrize(
    "filename,msg",
    [(1, 'filename needs to be a string'),
     ('file.rnd', 'The file is not a fit ride.'),
     ('file.fit', 'The file does not exist.')])
def test_check_check_filename_error(filename, msg):
    with pytest.raises(ValueError, message=msg):
        check_filename_fit(filename)


def test_check_filename_fit():
    filename = load_fit()[0]
    my_filename = check_filename_fit(filename)
    assert my_filename == filename
