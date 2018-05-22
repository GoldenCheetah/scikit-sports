"""Base classes for data management."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Cedric Lemaitre
# License: MIT

import numpy as np
import pandas as pd

from .extraction import activity_power_profile
from .io import bikeread
from .utils import validate_filenames


class Rider(object):
    """User interface for a rider.

    User interface to easily add, remove, compute information related to power.

    Read more in the :ref:`User Guide <record_power_profile>`.

    Parameters
    ----------
    n_jobs : int, (default=1)
        The number of workers to use for the different processing.

    Attributes
    ----------
    power_profile_ : DataFrame
        DataFrame containing all information regarding the power-profile of a
        rider for each ride.

    """

    def __init__(self, n_jobs=1):
        self.n_jobs = n_jobs
        self.power_profile_ = None

    def add_activities(self, filenames):
        """Compute the power-profile for each activity and add it to the
        current power-profile.

        Parameters
        ----------
        filenames : str or list of str
            A string a list of string to the file to read. You can use
            wildcards to automatically check several files.

        Returns
        -------
        None

        Examples
        --------
        >>> from sksports.datasets import load_fit
        >>> from sksports.base import Rider
        >>> rider = Rider()
        >>> rider.add_activities(load_fit()[0])
        >>> rider.power_profile_.head()
                          2014-05-07 12:26:22
        cadence 00:00:01            78.000000
                00:00:02            64.000000
                00:00:03            62.666667
                00:00:04            62.500000
                00:00:05            64.400000

        """
        filenames = validate_filenames(filenames)
        activities_pp = [activity_power_profile(bikeread(f))
                         for f in filenames]
        activities_pp = pd.concat(activities_pp, axis=1)

        if self.power_profile_ is not None:
            try:
                self.power_profile_ = self.power_profile_.join(activities_pp,
                                                               how='outer')
            except ValueError as e:
                if 'columns overlap but no suffix specified' in e.args[0]:
                    raise ValueError('One of the activity was already added'
                                     ' to the rider power-profile. Remove this'
                                     ' activity before to try to add it.')
                else:
                    raise
        else:
            self.power_profile_ = activities_pp

    def delete_activities(self, dates, time_comparison=False):
        """Delete the activities power-profile from some specific dates.

        Parameters
        ----------
        dates : list/tuple of datetime-like or str
            The dates of the activities to be removed. The format expected is:

            * datetime-like or str: a single activity will be deleted.
            * a list of datetime-like or str: each activity for which the date
              is contained in the list will be deleted.
            * a tuple of datetime-like or str ``(start_date, end_date)``: the
              activities for which the dates are included in the range will be
              deleted.

        time_comparison : bool, optional
            Whether to make a strict comparison using time or to relax to
            constraints with only the date.

        Returns
        -------
        None

        Examples
        --------
        >>> from sksports.datasets import load_rider
        >>> from sksports import Rider
        >>> rider = Rider.from_csv(load_rider())
        >>> rider.delete_activities('07 May 2014')
        >>> print(rider)
        RIDER INFORMATION:
         power-profile:
                           2014-05-11 09:39:38  2014-07-26 16:50:56
        cadence 00:00:01           100.000000            60.000000
                00:00:02            89.000000            58.000000
                00:00:03            68.333333            56.333333
                00:00:04            59.500000            59.250000
                00:00:05            63.200000            61.000000

        """
        def _strict_comparison(dates_pp, date, strict_equal):
            if strict_equal:
                return dates_pp == date
            else:
                return np.bitwise_and(
                    dates_pp >= date,
                    dates_pp <= pd.Timestamp(date) + pd.DateOffset(1))

        if isinstance(dates, tuple):
            if len(dates) != 2:
                raise ValueError("Wrong tuple format. Expecting a tuple of"
                                 " format (start_date, end_date). Got {!r}"
                                 " instead.".format(dates))
            mask_date = np.bitwise_and(
                self.power_profile_.columns >= dates[0],
                self.power_profile_.columns <= pd.Timestamp(dates[1]) +
                pd.DateOffset(1))
        elif isinstance(dates, list):
            mask_date = np.any(
                [_strict_comparison(self.power_profile_.columns, d,
                                    time_comparison)
                 for d in dates], axis=0)
        else:
            mask_date = _strict_comparison(self.power_profile_.columns, dates,
                                           time_comparison)

        mask_date = np.bitwise_not(mask_date)
        self.power_profile_ = self.power_profile_.loc[:, mask_date]

    def record_power_profile(self, range_dates=None, columns=None):
        """Compute the record power-profile.

        Parameters
        ----------
        range_dates : tuple of datetime-like or str, optional
            The start and end date to consider when computing the record
            power-profile. By default, all data will be used.

        columns : array-like or None, optional
            Name of data field to return. By default, all available data will
            be returned.

        Returns
        -------
        record_power_profile : DataFrame
            Record power-profile taken between the range of dates.

        Examples
        --------
        >>> from sksports import Rider
        >>> from sksports.datasets import load_rider
        >>> rider = Rider.from_csv(load_rider())
        >>> record_power_profile = rider.record_power_profile()
        >>> record_power_profile.head() # doctest: +NORMALIZE_WHITESPACE
                    cadence      distance  elevation  heart-rate       power
        00:00:01  60.000000  27162.600000        NaN         NaN  750.000000
        00:00:02  58.000000  27163.750000        NaN         NaN  741.000000
        00:00:03  56.333333  27164.586667        NaN         NaN  731.666667
        00:00:04  59.250000  27163.402500        NaN         NaN  719.500000
        00:00:05  61.000000  27162.142000        NaN         NaN  712.200000

        This is also possible to give a range of dates to compute the record
        power-profile. We can also select some specific information.

        >>> record_power_profile = rider.record_power_profile(
        ...     range_dates=('07 May 2014', '11 May 2014'),
        ...     columns=['power', 'cadence'])
        >>> record_power_profile.head()
                     cadence   power
        00:00:01  100.000000  717.00
        00:00:02   89.000000  717.00
        00:00:03   68.333333  590.00
        00:00:04   59.500000  552.25
        00:00:05   63.200000  552.60

        """
        if range_dates is None:
            mask_date = np.ones_like(self.power_profile_.columns,
                                     dtype=bool)
        else:
            mask_date = np.bitwise_and(
                self.power_profile_.columns >= range_dates[0],
                self.power_profile_.columns <= pd.Timestamp(range_dates[1]) +
                pd.DateOffset(1))

        if columns is None:
            columns = self.power_profile_.index.levels[0]

        pp_idxmax = (self.power_profile_.loc['power']
                                        .loc[:, mask_date]
                                        .idxmax(axis=1)
                                        .dropna())
        rpp = {}
        for dt in columns:
            data = self.power_profile_.loc[dt].loc[:, mask_date]
            rpp[dt] = pd.Series(
                [data.loc[date_idx]
                 for date_idx in pp_idxmax.iteritems()],
                index=data.index[:pp_idxmax.size])

        return pd.DataFrame(rpp)

    @classmethod
    def from_csv(cls, filename, n_jobs=1):
        """Load rider information from a CSV file.

        Parameters
        ----------
        filename : str
            The path to the CSV file.

        n_jobs : int, (default=1)
            The number of workers to use for the different processing.

        Returns
        -------
        rider : sksports.Rider
            The :class:`sksports.Rider` instance.

        Examples
        --------
        >>> from sksports.datasets import load_rider
        >>> from sksports import Rider
        >>> rider = Rider.from_csv(load_rider())
        >>> print(rider) # doctest: +NORMALIZE_WHITESPACE
        RIDER INFORMATION:
         power-profile:
                           2014-05-07 12:26:22  2014-05-11 09:39:38  \\
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

        """
        df = pd.read_csv(filename, index_col=[0, 1])
        df.columns = pd.to_datetime(df.columns)
        df.index = pd.MultiIndex(levels=[df.index.levels[0],
                                         pd.to_timedelta(df.index.levels[1])],
                                 labels=df.index.labels,
                                 name=[None, None])
        rider = cls(n_jobs=n_jobs)
        rider.power_profile_ = df
        return rider

    def to_csv(self, filename):
        """Drop the rider information into a CSV file.

        Parameters
        ----------
        filename : str
            The path to the CSV file.

        Returns
        -------
        None

        Examples
        --------
        >>> from sksports.datasets import load_fit
        >>> from sksports import Rider
        >>> rider = Rider(n_jobs=-1)
        >>> rider.add_activities(load_fit()[:1])
        >>> print(rider)
        RIDER INFORMATION:
         power-profile:
                           2014-05-07 12:26:22
        cadence 00:00:01            78.000000
                00:00:02            64.000000
                00:00:03            62.666667
                00:00:04            62.500000
                00:00:05            64.400000

        """
        self.power_profile_.to_csv(filename, date_format='%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return 'RIDER INFORMATION:\n power-profile:\n {}'.format(
            self.power_profile_.head())
