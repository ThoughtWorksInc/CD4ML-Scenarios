from sklearn import metrics
import numpy as np

# TODO: add others
# TODO: add ability to include generic functions


def r2_score(true_target, prediction):
    # R2 metric
    return metrics.r2_score(y_true=true_target, y_pred=prediction)


def rms_score(true_target, prediction):
    # Root mean square metric
    return np.sqrt(((prediction - true_target)**2).mean())


def mad_score(true_target, prediction):
    # mean absolute deviation metric
    return abs(prediction - true_target).mean()


def get_validation_metrics(metric_names, true_prediction_function):

    print('Getting predictions')
    data = list(true_prediction_function())
    print('Done with predictions')
    assert len(data) > 0
    true_target, prediction = zip(*data)

    true_target = np.array(true_target)
    prediction = np.array(prediction)

    n_validated = len(true_target)
    print('n_validated: %s' % n_validated)

    validation_metrics = {}
    if 'r2_score' in metric_names:
        print('r2_scoring')
        validation_metrics['r2_score'] = r2_score(true_target, prediction)

    if 'rms_score' in metric_names:
        print('rms_scoring')
        validation_metrics['rms_score'] = rms_score(true_target, prediction)

    if 'mad_score' in metric_names:
        print('mad_scoring')
        validation_metrics['mad_score'] = mad_score(true_target, prediction)

    if 'num_validated' in metric_names:
        validation_metrics['num_validated'] = n_validated

    print('Done validation metrics')

    return validation_metrics
