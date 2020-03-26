from csv import DictReader
from cd4ml.filenames import file_names
from cd4ml.one_hot.one_hot_encoder import OneHotEncoder


def stream_raw_data():
    filename = file_names['raw_data']
    return (dict(row) for row in DictReader(open(filename, 'r')))


def process(row_in):
    row = {'id': row_in['id'],
           'item_nbr': row_in['item_nbr'],
           'unit_sales': max(0.0, float(row_in['unit_sales'])),
           'date': row_in['date'],
           'year': row_in['year'],
           'month': row_in['month'],
           'day': row_in['day'],
           'class': row_in['class'],
           'family': row_in['family'],
           'perishable': int(row_in['perishable'] == '1'),
           'transactions': int(row_in['transactions']),
           'dayofweek': row_in['dayofweek'],
           'days_til_end_of_data': int(row_in['days_til_end_of_data']),
           'dayoff': int(row_in['dayoff'] == 'True')
           }

    return row


def stream_data():
    return (process(row) for row in stream_raw_data())


def get_encoder_from_stream(stream):
    categorical_n_levels_dict_all = {'item_nbr': 10000000000,
                                     'year': 50,
                                     'month': 13,
                                     'day': 370,
                                     'class': 600,
                                     'family': 100,
                                     'dayofweek': 10}

    categorical_n_levels_dict = categorical_n_levels_dict_all

    numeric_columns = ['unit_sales', 'perishable', 'transactions',
                       'days_til_end_of_data', 'dayoff']

    encoder = OneHotEncoder(categorical_n_levels_dict, numeric_columns)
    encoder.load_from_data_stream(stream)
    return encoder


def get_encoder():
    stream = stream_data()
    return get_encoder_from_stream(stream)
