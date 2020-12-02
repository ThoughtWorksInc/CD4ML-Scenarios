import logging
from cd4ml.available_models import get_algorithm_class

logger = logging.getLogger(__name__)


def train_model(encoded_train_data, target, model_name, params, seed=None):

    model_class = get_algorithm_class(model_name)

    logger.info("Training {} model".format(model_name))
    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(encoded_train_data, target)
    return trained_model


def get_trained_model(algorithm_name,
                      algorithm_params,
                      encoded_train_data,
                      target_data,
                      seed):

    n_rows = len(encoded_train_data)
    n_cols = len(encoded_train_data[0])
    logger.info('n_rows: %s, n_cols: %s' % (n_rows, n_cols))

    trained_model = train_model(encoded_train_data, target_data, algorithm_name,
                                algorithm_params, seed=seed)

    return trained_model
