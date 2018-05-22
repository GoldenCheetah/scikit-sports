Scikit-cycling
==============

.. image:: https://travis-ci.org/scikit-sports/scikit-sports.svg?branch=master
    :target: https://travis-ci.org/scikit-sports/scikit-sports

.. image:: https://ci.appveyor.com/api/projects/status/f2mvtb9y1mcy99vg?svg=true
    :target: https://ci.appveyor.com/project/glemaitre/scikit-sports

.. image:: https://readthedocs.org/projects/scikit-sports/badge/?version=latest
    :target: http://scikit-sports.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/scikit-sports/scikit-sports/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/scikit-sports/scikit-sports

.. image:: https://badges.gitter.im/Join%20Chat.svg
  :target: https://gitter.im/scikit-sports/Lobby?utm_source=share-link&utm_medium=link&utm_cam

Installation
------------

Dependencies
~~~~~~~~~~~~

Scikit-cycling requires:

* scipy
* numpy
* pandas
* six
* fit-parse
* joblib
* scikit-learn


Installation
~~~~~~~~~~~~

``scikit-sports`` is currently available on the PyPi’s reporitories and you can
install it via pip::

  pip install -U scikit-sports

The package is release also in conda-forge::

  conda install -c conda-forge scikit-sports

If you prefer, you can clone it and run the ``setup.py`` file. Use the
following commands to get a copy from Github and install all dependencies::

  git clone https://github.com/scikit-sports/scikit-sports.git
  cd scikit-sports
  pip install .

Or install using ``pip`` and GitHub::

  pip install -U git+https://github.com/scikit-sports/scikit-sports.git
