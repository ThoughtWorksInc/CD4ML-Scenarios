from sklearn import metrics
import numpy as np
import logging
logger = logging.getLogger(__name__)

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
    logger.info('Getting predictions')
    data = list(true_prediction_function())
    logger.info('Done with predictions')
    assert len(data) > 0
    true_target, prediction = zip(*data)

    true_target = np.array(true_target)
    prediction = np.array(prediction)

    n_validated = len(true_target)
    logger.info('n_validated: %s' % n_validated)

    validation_metrics = {}
    if 'r2_score' in metric_names:
        validation_metrics['r2_score'] = r2_score(true_target, prediction)
        logger.info('r2_score : {}'.format(validation_metrics['r2_score']))

    if 'rms_score' in metric_names:
        validation_metrics['rms_score'] = rms_score(true_target, prediction)
        logger.info('rms_scoring: {}'.format(validation_metrics['rms_score']))

    if 'mad_score' in metric_names:
        validation_metrics['mad_score'] = mad_score(true_target, prediction)
        logger.info('mad_scoring: {}'.format(validation_metrics['mad_score']))

    if 'num_validated' in metric_names:
        validation_metrics['num_validated'] = n_validated

    logger.info('Done validation metrics')

    return validation_metrics
