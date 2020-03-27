import os
from csv import DictReader
from cd4ml.filenames import file_names
from cd4ml.one_hot.one_hot_encoder import OneHotEncoder

# use just a small number of items?
use_filter = True


def in_small_item_list(row):
    items = {"99197", "105574", "1963838"}
    return row['item_nbr'] in items


def stream_raw_data():
    filename = file_names['raw_data']
    if use_filter:
        filter_func = in_small_item_list
    else:
        def filter_func(_):
            return True

    return (dict(row) for row in DictReader(open(filename, 'r'))
            if filter_func(row))


def process(row_in):
    row = {'item_nbr': row_in['item_nbr'],
           'unit_sales': max(0.0, float(row_in['unit_sales'])),
           'date': row_in['date'],
           'year': row_in['year'],
           'month': row_in['month'],
           'day': row_in['day'],
           'class': row_in['class'],
           'family': row_in['family'],
           'perishable': int(row_in['perishable'] == '1'),
           'dayofweek': row_in['dayofweek'],
           'days_til_end_of_data': int(row_in['days_til_end_of_data']),
           'dayoff': int(row_in['dayoff'] == 'True')}

    return row


def stream_data():
    return (process(row) for row in stream_raw_data())


def get_encoder_from_stream(stream):
    # batch step
    categorical_n_levels_dict_all = {'item_nbr': 10000000000,
                                     'year': 50,
                                     'month': 13,
                                     'day': 370,
                                     'class': 600,
                                     'family': 100,
                                     'dayofweek': 10}

    categorical_n_levels_dict = categorical_n_levels_dict_all

    numeric_columns = ['perishable',
                       'days_til_end_of_data',
                       'dayoff']

    encoder = OneHotEncoder(categorical_n_levels_dict, numeric_columns)
    encoder.load_from_data_stream(stream)
    return encoder


def get_encoder(write=True, read_from_file=False):
    # batch step
    encoder_file = file_names['encoder']
    if os.path.exists(encoder_file) and read_from_file:
        print('Reading encoder from : %s' % encoder_file)
        encoder_from_file = OneHotEncoder([], [])
        encoder_from_file.load_from_file(encoder_file)
        return encoder_from_file

    print('Building encoder')
    stream = stream_data()
    encoder = get_encoder_from_stream(stream)

    if write:
        print('Writing encoder to: %s' % encoder_file)
        encoder.save(encoder_file)

    return encoder
