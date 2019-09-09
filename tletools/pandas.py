"""
The module :mod:`tletools.pandas` provides convenience functions to load
two-line element set files into :class:`pandas.DataFrame`'s.'
"""

import pandas as pd

from .tle import TLE
from .utils import partition, dt_dt64_Y, dt_td64_us


def load_dataframe(filename, *, epoch=True):
    """Load multiple TLEs from one or more files and return a :class:`pandas.DataFrame`."""
    if isinstance(filename, str):
        with open(filename) as fp:
            df = pd.DataFrame(TLE.from_lines(*l012).asdict()
                              for l012 in partition(fp, 3))
            if epoch:
                add_epoch(df)
            return df
    else:
        df = pd.concat([TLE.load_dataframe(fn, epoch=False) for fn in filename],
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
    df['epoch'] = year + days
