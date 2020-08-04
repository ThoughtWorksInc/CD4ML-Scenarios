from cd4ml.model_utils import get_model_class


def train_model(encoded_train_data, target, model_name, params, seed=None):
    model_class = get_model_class(model_name)

    print("Training %s model" % model_name)
    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(encoded_train_data, target)
    return trained_model


def get_trained_model(algorithm_name,
                      algorithm_params,
                      encoded_train_data,
                      track,
                      target_data,
                      seed):

    n_rows = len(encoded_train_data)
    n_cols = len(encoded_train_data[0])
    print('n_rows: %s, n_cols: %s' % (n_rows, n_cols))

    if track is not None:
        track.log_ml_params(algorithm_params)

    trained_model = train_model(encoded_train_data, target_data, algorithm_name,
                                algorithm_params, seed=seed)

    return trained_model
