import os
from cd4ml.filenames import file_names
from cd4ml.one_hot.one_hot_encoder import OneHotEncoder
from cd4ml.readers.streamer import DataStreamer


def stream_data(pipeline_params):
    """
    The only way that data should be read in the pipeline is by calling this
    and reading from the stream
    :param pipeline_params: parameters for everything in pipeline
    :return: a stream of data from a source specified in pipeline_params
    """
    configuration = pipeline_params["data_reader"]
    data_streamer = DataStreamer(configuration)
    data = data_streamer.stream_data()
    for row in data:
        yield data_streamer.process(row)

    data_streamer.close()


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


def get_encoder(pipeline_params, write=True, read_from_file=False):
    # batch step
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
