import os
from cd4ml.filenames import file_names
from cd4ml.one_hot.one_hot_encoder import OneHotEncoder
from cd4ml.readers.streamer import DataStreamer


def process(row_in):
    return {'item_nbr': row_in['item_nbr'],
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


def filter_func(row):
    """
    Filter function for data
    :param row: row, dictionary
    :return: True if it should be included, False if skipped
    """
    items_to_keep = {"99197", "105574", "1963838"}
    if row['item_nbr'] in items_to_keep:
        return True

    return False


def stream_data(pipeline_params, apply_filter=True):
    """
    The only way that data should be read in the pipeline is by calling this
    and reading from the stream
    :param pipeline_params: parameters for everything in pipeline
    :param apply_filter: if true (default), filter the rows
    :return: a stream of data from a source specified in pipeline_params
    """
    data_source = pipeline_params["data_source"]
    data_streamer = DataStreamer(data_source)
    data = data_streamer.stream_data()
    for row in data:
        if apply_filter and not filter_func(row):
            # does not pass filter, skip
            continue

        yield process(row)


def get_encoder_from_stream(stream):
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


def get_encoder(pipeline_params, write=True, read_from_file=False):
    encoder_file = file_names['encoder']
    if os.path.exists(encoder_file) and read_from_file:
        print('Reading encoder from : %s' % encoder_file)
        encoder_from_file = OneHotEncoder([], [])
        encoder_from_file.load_from_file(encoder_file)
        return encoder_from_file

    print('Building encoder')
    stream = stream_data(pipeline_params)
    encoder = get_encoder_from_stream(stream)

    if write:
        print('Writing encoder to: %s' % encoder_file)
        encoder.save(encoder_file)

    return encoder
