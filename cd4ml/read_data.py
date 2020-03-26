import numpy as np
import pandas as pd


def read_raw_data(filename):
    dtypes = {'class': np.str,
              'date': np.str,
              'day': np.str,
              'dayoff': np.int64,
              'dayofweek': np.str,
              'days_til_end_of_data': np.int64,
              'family': np.str,
              'id': np.str,
              'item_nbr': np.str,
              'month': np.str,
              'perishable': np.int64,
              'transactions': np.int64,
              'unit_sales': np.float64,
              'year': np.str}

    return pd.read_csv(filename, dtype=dtypes)


def transform_data(data):
    data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
    data.loc[data.unit_sales < 0, 'unit_sales'] = 0

    # TODO: add features
