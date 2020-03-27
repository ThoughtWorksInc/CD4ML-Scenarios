from sklearn import metrics
import os
import json
import joblib
from cd4ml import tracking
from cd4ml.read_data import stream_data, get_encoder
from cd4ml.splitter import get_cutoff_dates, train_filter, validate_filter
from cd4ml.model_utils import get_model_class, get_model_params
from cd4ml.filenames import file_names


def train_model(train_data, target, model_name, params, seed=None):
    model_class = get_model_class(model_name)

    print("Training %s model" % model_name)
    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(train_data, target)
    return trained_model, params


def run_ml_model(encoder, track, date_cutoff, model_name='random_forest', seed=None):
    target_name = 'unit_sales'

    train_stream = (row for row in stream_data() if train_filter(row, date_cutoff))
    encoded_train_stream = encoder.encode_data_stream(train_stream)

    print('Encoding data')
    # batch step, read it all in
    encoded_train_data = list(encoded_train_stream)
    # read it all in
    print('Getting target')
    target = [row[target_name] for row in stream_data() if train_filter(row, date_cutoff)]

    # with tracking.track() as track:

    params = get_model_params(model_name)

    track.set_model(model_name)
    track.log_params(params)

    trained_model, params = train_model(encoded_train_data, target, model_name, params, seed=seed)

    return trained_model, params


def write_predictions_and_score(evaluation_metrics):
    filename = 'results/metrics.json'
    print("Writing to {}".format(filename))
    if not os.path.exists('results'):
        os.makedirs('results')
    with open(filename, 'w+') as score_file:
        json.dump(evaluation_metrics, score_file)


def write_model(model):
    filename = file_names['model']
    print("Writing to {}".format(filename))
    joblib.dump(model, filename)


def validate(model, encoder, track, date_cutoff, max_date):
    target_name = 'unit_sales'
    validate_stream = (row for row in stream_data() if validate_filter(row, date_cutoff, max_date))
    encoded_validate_stream = encoder.encode_data_stream(validate_stream)
    validation_predictions = [model.predict([row]) for row in encoded_validate_stream]

    target = [row[target_name] for row in stream_data() if validate_filter(row, date_cutoff, max_date)]

    print("Calculating metrics")
    evaluation_metrics = {'r2_score': metrics.r2_score(y_true=target, y_pred=validation_predictions)}
    track.log_metrics(evaluation_metrics)

    write_predictions_and_score(evaluation_metrics)

    print("Evaluation done with metrics {}.".format(
        json.dumps(evaluation_metrics)))

    write_model(model)


def run_all(model_name='random_forest', seed=None):
    encoder = get_encoder(write=True, read_from_file=False)
    date_cutoff, max_date = get_cutoff_dates(57)

    with tracking.track() as track:
        trained_model, params = run_ml_model(encoder, track, date_cutoff, model_name=model_name, seed=seed)
        validate(trained_model, encoder, track, date_cutoff, max_date)
