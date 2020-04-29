import os
import json
import joblib
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


def write_validation_info(validation_metrics, trained_model, track,
                          true_validation_target,
                          validation_predictions):

    track.log_metrics(validation_metrics)
    fluentd_logger.log('validation_metrics', validation_metrics)

    write_predictions_and_score(validation_metrics)

    print("Evaluation done with metrics {}.".format(
        json.dumps(validation_metrics)))

    write_model(trained_model)

    make_validation_plot(true_validation_target, validation_predictions, track)
