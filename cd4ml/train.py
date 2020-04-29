from cd4ml.model_utils import get_model_class
from cd4ml import tracking


track = tracking.track()


def train_model(train_data, target, model_name, params, seed=None):
    model_class = get_model_class(model_name)

    print("Training %s model" % model_name)
    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(train_data, target)
    return trained_model


def get_trained_model(pipeline_params, training_stream_function, encoder):
    encoded_train_stream = encoder.encode_data_stream(training_stream_function())

    print('Encoding data')
    # batch step, read it all in
    encoded_train_data = list(encoded_train_stream)

    print('Getting target')
    # read it all in
    target_name = pipeline_params['ml_fields']['target_name']
    target = [row[target_name] for row in training_stream_function()]

    model_name = pipeline_params['problem_params']['model_name']
    params = pipeline_params['model_params'][model_name]

    track.log_ml_params(params)
    track.log_pipeline_params(pipeline_params)

    seed = pipeline_params['problem_params']['random_seed']
    trained_model = train_model(encoded_train_data, target, model_name, params, seed=seed)

    return trained_model
