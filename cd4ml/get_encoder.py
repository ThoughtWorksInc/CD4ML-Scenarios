import os
from cd4ml.filenames import file_names
from wickedhot import OneHotEncoder


def get_encoder_from_stream(stream, ml_fields):
    # ensure target variable is not included as input variable
    target = ml_fields['target_name']
    categorical = {k: v for k, v in ml_fields['categorical'].items() if k != target}
    numerical = [field for field in ml_fields['numerical'] if field != target]

    encoder = OneHotEncoder(categorical, numerical)
    encoder.load_from_data_stream(stream)
    return encoder


def get_encoder(stream, ml_fields, write=True, read_from_file=False):
    encoder_file = file_names['encoder']
    if os.path.exists(encoder_file) and read_from_file:
        print('Reading encoder from : %s' % encoder_file)
        encoder_from_file = OneHotEncoder([], [])
        encoder_from_file.load_from_file(encoder_file)
        return encoder_from_file

    print('Building encoder')
    encoder = get_encoder_from_stream(stream, ml_fields)

    if write:
        print('Writing encoder to: %s' % encoder_file)
        encoder.save(encoder_file)

    return encoder
