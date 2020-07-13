from sklearn import metrics
import os
import json
import joblib
from cd4ml.read_data import stream_data
from cd4ml.splitter import validate_filter
from cd4ml.filenames import file_names
from cd4ml.validation_plots import make_validation_plot
from cd4ml.fluentd_logging import FluentdLogger

fluentd_logger = FluentdLogger()


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


def validate(pipeline_params, model, encoder, track, date_cutoff, max_date):
    target_name = 'unit_sales'
    validate_stream = (row for row in stream_data(pipeline_params)
                       if validate_filter(row, date_cutoff, max_date))

    encoded_validate_stream = encoder.encode_data_stream(validate_stream)
    validation_predictions = [float(model.predict([row])) for row in encoded_validate_stream]

    target = [row[target_name] for row in stream_data(pipeline_params)
              if validate_filter(row, date_cutoff, max_date)]

    print("Calculating metrics")
    validation_metrics = {'r2_score': metrics.r2_score(y_true=target, y_pred=validation_predictions)}

    track.log_metrics(validation_metrics)
    fluentd_logger.log('validation_metrics', validation_metrics)

    write_predictions_and_score(validation_metrics)

    print("Evaluation done with metrics {}.".format(
        json.dumps(validation_metrics)))

    write_model(model)
    make_validation_plot(target, validation_predictions, track)
