from sklearn import metrics
import numpy as np

# TODO: add others
# TODO: add ability to include generic functions


def r2_score(true_prediction):
    # R2 metric
    true_target, prediction = zip(*true_prediction)
    return metrics.r2_score(y_true=true_target, y_pred=prediction)


def rms_score(true_prediction):
    # Root mean square metric
    true_target, prediction = zip(*true_prediction)
    true_target = np.array(true_target)
    prediction = np.array(prediction)
    return np.sqrt(((prediction - true_target)**2).mean())


def mad_score(true_prediction):
    # mean absolute deviation metric
    true_target, prediction = zip(*true_prediction)
    true_target = np.array(true_target)
    prediction = np.array(prediction)
    return abs(prediction - true_target).mean()


def get_validation_metrics(metric_names, true_prediction_function):
    validation_metrics = {}
    if 'r2_score' in metric_names:
        validation_metrics['r2_score'] = r2_score(true_prediction_function())

    if 'rms_score' in metric_names:
        validation_metrics['rms_score'] = rms_score(true_prediction_function())

    if 'mad_score' in metric_names:
        validation_metrics['mad_score'] = mad_score(true_prediction_function())

    return validation_metrics
