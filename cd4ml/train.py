from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso

import logging
logger = logging.getLogger(__name__)


def get_model_class(model_name):
    model_classes = {
        'random_forest': RandomForestRegressor,
        'adaboost': AdaBoostRegressor,
        'gradient_boosting': GradientBoostingRegressor,
        'decision_tree': DecisionTreeRegressor,
        'ridge': Ridge,
        'lasso': Lasso
    }

    return model_classes[model_name]


def train_model(encoded_train_data, target, model_name, params, seed=None):

    # print(encoded_train_data[0:3])

    model_class = get_model_class(model_name)

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
