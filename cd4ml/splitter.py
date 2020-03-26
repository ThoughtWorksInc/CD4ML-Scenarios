import pandas as pd
from datetime import datetime
from cd4ml.filenames import file_names
from cd4ml.read_data import stream_data


def date_string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def date_string_to_date_pandas(date_string):
    return pd.to_datetime(date_string, format="%Y-%m-%d")


def get_validation_period(latest_date_train, days_back=15):
    latest_date = date_string_to_date(latest_date_train)
    # for Kaggle we want from Wednesday to Thursday for a 15 day period
    offset = (latest_date.weekday() - 3) % 7
    end_of_validation_period = latest_date - pd.DateOffset(days=offset)
    begin_of_validation_period = end_of_validation_period - \
        pd.DateOffset(days=days_back)
    return begin_of_validation_period, end_of_validation_period


def split_validation_train_by_validation_period(train, validation_begin_date, validation_end_date):
    train_validation = train[(date_string_to_date_pandas(train['date']) >= validation_begin_date) & (
        date_string_to_date_pandas(train['date']) <= validation_end_date)]

    train_train = train[date_string_to_date_pandas(train['date']) < validation_begin_date]
    return train_train, train_validation


def write_data(table, filename):
    print("Writing to data/splitter/{}".format(filename))
    table.to_csv(filename, index=False)


def run_splitter():
    print("Loading data...")
    data = read_raw_data(file_names['raw_data'])

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


def get_cutoff_dates():
    max_date = '1500-01-01'
    stream = read_raw_data



def split_stream(stream, date_cutoff):
    pass
