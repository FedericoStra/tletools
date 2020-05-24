"""
The module :mod:`tletools.pandas` provides convenience functions to load
two-line element set files into :class:`pandas.DataFrame`'s.'

Given a file ``oneweb.txt`` with the following contents::

    ONEWEB-0012
    1 44057U 19010A   19290.71624163  .00000233  00000-0  58803-3 0  9997
    2 44057  87.9055  22.9851 0002022  94.9226 265.2135 13.15296315 30734
    ONEWEB-0010
    1 44058U 19010B   19290.71785289  .00000190  00000-0  47250-3 0  9991
    2 44058  87.9054  22.9846 0002035  97.1333 263.0028 13.15294565 30783
    ONEWEB-0008
    1 44059U 19010C   19290.86676214 -.00000034  00000-0 -12353-3 0  9990
    2 44059  87.9055  22.9563 0001967  95.9628 264.1726 13.15300216 30897
    ONEWEB-0007
    1 44060U 19010D   19290.87154896  .00000182  00000-0  45173-3 0  9998
    2 44060  87.9067  22.9618 0001714  97.9802 262.1523 13.15299021 30927
    ONEWEB-0006
    1 44061U 19010E   19290.72095254  .00000179  00000-0  44426-3 0  9991
    2 44061  87.9066  22.9905 0001931  95.0539 265.0811 13.15294588 30940
    ONEWEB-0011
    1 44062U 19010F   19291.17894923  .00000202  00000-0  50450-3 0  9993
    2 44062  87.9056  22.8943 0002147  94.8298 265.3077 13.15300820 31002

you can load the TLEs into a :class:`pandas.DataFrame` by using

>>> load_dataframe("oneweb.txt") # doctest: +SKIP
          name  norad classification int_desig  epoch_year   epoch_day         dn_o2  ddn_o6     bstar  set_num      inc     raan       ecc     argp         M          n  rev_num                      epoch
0  ONEWEB-0012  44057              U    19010A        2019  290.716242  2.330000e-06     0.0  0.000588      999  87.9055  22.9851  0.000202  94.9226  265.2135  13.152963     3073 2019-10-17 17:11:23.276832
1  ONEWEB-0010  44058              U    19010B        2019  290.717853  1.900000e-06     0.0  0.000472      999  87.9054  22.9846  0.000204  97.1333  263.0028  13.152946     3078 2019-10-17 17:13:42.489696
2  ONEWEB-0008  44059              U    19010C        2019  290.866762 -3.400000e-07     0.0 -0.000124      999  87.9055  22.9563  0.000197  95.9628  264.1726  13.153002     3089 2019-10-17 20:48:08.248896
3  ONEWEB-0007  44060              U    19010D        2019  290.871549  1.820000e-06     0.0  0.000452      999  87.9067  22.9618  0.000171  97.9802  262.1523  13.152990     3092 2019-10-17 20:55:01.830144
4  ONEWEB-0006  44061              U    19010E        2019  290.720953  1.790000e-06     0.0  0.000444      999  87.9066  22.9905  0.000193  95.0539  265.0811  13.152946     3094 2019-10-17 17:18:10.299456
5  ONEWEB-0011  44062              U    19010F        2019  291.178949  2.020000e-06     0.0  0.000504      999  87.9056  22.8943  0.000215  94.8298  265.3077  13.153008     3100 2019-10-18 04:17:41.213472

You can also load multiple files into a single :class:`pandas.DataFrame` with

>>> from glob import glob
>>> load_dataframe(glob("*.txt")) # doctest: +SKIP
"""

import pandas as pd

from .tle import TLE
from .utils import partition, dt_dt64_Y, dt_td64_us


def load_dataframe(filename, *, computed=False, epoch=True):
    """Load multiple TLEs from one or more files and return a :class:`pandas.DataFrame`.

    :param filename: A single filename (:class:`str`) or an iterable producing filenames.
    :type filename: str or iterable
    :returns: A :class:`pandas.DataFrame` with all the loaded TLEs.

    **Examples**

    >>> load_dataframe("oneweb.txt") # doctest: +SKIP

    >>> load_dataframe(["oneweb.txt", "starlink.txt"]) # doctest: +SKIP

    >>> from glob import glob
    >>> load_dataframe(glob("*.txt")) # doctest: +SKIP
    """
    if isinstance(filename, str):
        with open(filename) as fp:
            df = pd.DataFrame(TLE.from_lines(*l012).asdict(computed=computed)
                              for l012 in partition(fp, 3))
            if epoch:
                add_epoch(df)
            return df
    else:
        df = pd.concat(
            [load_dataframe(fn, computed=computed, epoch=False) for fn in filename],
            ignore_index=True, join='inner', copy=False)
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        add_epoch(df)
        return df


def add_epoch(df):
    """Add a column ``'epoch'`` to a dataframe.

    `df` must have columns ``'epoch_year'`` and ``'epoch_day'``, from which the
    column ``'epoch'`` is computed.

    :param pandas.DataFrame df: :class:`pandas.DataFrame` instance to modify.

    **Example**

    >>> from pandas import DataFrame
    >>> df = DataFrame([[2018, 31.2931], [2019, 279.3781]],
    ...                columns=['epoch_year', 'epoch_day'])
    >>> add_epoch(df)
    >>> df
       epoch_year  epoch_day                   epoch
    0        2018    31.2931 2018-01-31 07:02:03.840
    1        2019   279.3781 2019-10-06 09:04:27.840
    """
    years = (df.epoch_year.values - 1970).astype(dt_dt64_Y)
    days = ((df.epoch_day.values - 1) * 86400 * 1000000).astype(dt_td64_us)
    df['epoch'] = years + days
