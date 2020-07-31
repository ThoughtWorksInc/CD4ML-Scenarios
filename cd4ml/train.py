from cd4ml.model_utils import get_model_class


def train_model(encoded_train_data, target, model_name, params, seed=None):
    model_class = get_model_class(model_name)

    print("Training %s model" % model_name)
    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(encoded_train_data, target)
    return trained_model


def get_trained_model(pipeline_params,
                      encoded_train_data,
                      track,
                      target_data):

    n_rows = len(encoded_train_data)
    n_cols = len(encoded_train_data[0])
    print('n_rows: %s, n_cols: %s' % (n_rows, n_cols))

    model_name = pipeline_params['problem_params']['model_name']
    params = pipeline_params['model_params']

    if track is not None:
        track.log_pipeline_params(pipeline_params)
        track.log_ml_params(params)

    seed = pipeline_params['problem_params']['random_seed']

    trained_model = train_model(encoded_train_data, target_data, model_name, params, seed=seed)

    return trained_model
