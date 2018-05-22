.. _datasets:

.. currentmodule:: sksports

========
Datasets
========

:mod:`datasets` provides some toy datasets to play with.

FIT files
---------

There is a couple of FIT files which can be loaded using the function
:func:`datasets.load_fit`::

  >>> from sksports.datasets import load_fit
  >>> from sksports.io import bikeread
  >>> print('The filename of the FIT file is \n {}'.format(load_fit()[0]))
  The filename of the FIT file is 
   /home/lemaitre/Documents/code/toolbox/scikit-sports/sksports/datasets/data/2014-05-07-14-26-22.fit
  >>> ride = bikeread(load_fit()[0])  # load the first fit file

Rider instance
..............

To play with the :class:`rider`, we provide a rider file store in CSV. The
function :func:`datasets.load_rider` give access to this file::

  >>> from sksports import Rider
  >>> from sksports.datasets import load_rider
  >>> rider = Rider.from_csv(load_rider())
  >>> print(rider) # doctest: +NORMALIZE_WHITESPACE
  RIDER INFORMATION:
  power-profile:
                    2014-05-07 12:26:22  2014-05-11 09:39:38  \
  cadence 00:00:01            78.000000           100.000000   
          00:00:02            64.000000            89.000000   
          00:00:03            62.666667            68.333333   
          00:00:04            62.500000            59.500000   
          00:00:05            64.400000            63.200000   
  <BLANKLINE>
                    2014-07-26 16:50:56  
  cadence 00:00:01            60.000000  
          00:00:02            58.000000  
          00:00:03            56.333333  
          00:00:04            59.250000  
          00:00:05            61.000000
