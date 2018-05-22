Scikit-sports
=============

.. image:: https://travis-ci.org/GoldenCheetah/scikit-sports.svg?branch=master
    :target: https://travis-ci.org/GoldenCheetah/scikit-sports
             
.. image:: https://ci.appveyor.com/api/projects/status/tei5gfnma8uxf7u8?svg=true
    :target: https://ci.appveyor.com/project/glemaitre/scikit-sports

.. image:: https://readthedocs.org/projects/scikit-sports/badge/?version=latest
    :target: https://scikit-sports.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
      
.. image:: https://codecov.io/gh/GoldenCheetah/scikit-sports/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/GoldenCheetah/scikit-sports

Installation
------------

Dependencies
~~~~~~~~~~~~

Scikit-sports requires:

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
