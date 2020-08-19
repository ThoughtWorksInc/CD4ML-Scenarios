import os
from cd4ml.filenames import get_model_files
from wickedhot import OneHotEncoder
import logging
logger = logging.getLogger(__name__)


def get_encoder_from_stream(stream, ml_fields, omit_cols=None):
    # ensure target variable is not included as input variable
    target = ml_fields['target_name']
    categorical = {k: v for k, v in ml_fields['categorical'].items() if k != target}
    numerical = [field for field in ml_fields['numerical'] if field != target]

    encoder = OneHotEncoder(categorical, numerical, omit_cols=omit_cols)
    encoder.load_from_data_stream(stream)
    return encoder


def get_trained_encoder(stream, ml_fields, problem_name, write=True,
                        read_from_file=False, base_features_omitted=None):

    file_names = get_model_files(problem_name)
    encoder_file = file_names.get('encoder')

    if encoder_file and os.path.exists(encoder_file) and read_from_file:
        logger.info('Reading encoder from : {}'.format(encoder_file))
        logger.info(base_features_omitted)
        encoder_from_file = OneHotEncoder([], [], omit_cols=base_features_omitted)
        encoder_from_file.load_from_file(encoder_file)
        return encoder_from_file

    logger.info('Building encoder')
    encoder = get_encoder_from_stream(stream, ml_fields, omit_cols=base_features_omitted)

    if write:
        if encoder_file:
            logger.info('Writing encoder to: %s' % encoder_file)
            encoder.save(encoder_file)

    return encoder
