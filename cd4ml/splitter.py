import pandas as pd
import numpy as np
from cd4ml.filenames import file_names


def get_validation_period(latest_date_train, days_back=15):
    # for Kaggle we want from Wednesday to Thursday for a 15 day period
    offset = (latest_date_train.weekday() - 3) % 7
    end_of_validation_period = latest_date_train - pd.DateOffset(days=offset)
    begin_of_validation_period = end_of_validation_period - \
        pd.DateOffset(days=days_back)
    return begin_of_validation_period, end_of_validation_period


def split_validation_train_by_validation_period(train, validation_begin_date, validation_end_date):
    train_validation = train[(train['date'] >= validation_begin_date) & (
        train['date'] <= validation_end_date)]
    train_train = train[train['date'] < validation_begin_date]
    return train_train, train_validation


def write_data(table, filename):
    print("Writing to data/splitter/{}".format(filename))
    table.to_csv(filename, index=False)


def read_raw_data():
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

    data = pd.read_csv(file_names['raw_data'], dtype=dtypes)
    data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
    return data


def read_data():
    data = read_raw_data()
    data.loc[data.unit_sales < 0, 'unit_sales'] = 0

    # TODO: add features
    return data


def run_splitter():
    print("Loading data...")
    data = read_data()

    latest_date = data['date'].max()

    begin_of_validation, end_of_validation = get_validation_period(
        latest_date, days_back=57)

    print("Splitting data between {} and {}".format(
        begin_of_validation, end_of_validation))
    train, validation = split_validation_train_by_validation_period(data,
                                                                    begin_of_validation,
                                                                    end_of_validation)
    write_data(train, file_names['train'])

    write_data(validation, file_names['validation'])

    print("Finished splitting")
