from sklearn import metrics
import numpy as np
import logging
logger = logging.getLogger(__name__)

# TODO: add others
# TODO: add ability to include generic functions

# The actual functions


def r2_score(true_target, prediction):
    # R2 metric
    return metrics.r2_score(y_true=true_target, y_pred=prediction)


def rms_score(true_target, prediction):
    # Root mean square metric
    return np.sqrt(((np.array(prediction) - np.array(true_target))**2).mean())


def mad_score(true_target, prediction):
    # mean absolute deviation metric
    return abs(np.array(prediction) - np.array(true_target)).mean()


# classification

def f1_score(true_target, prediction):
    # mean absolute deviation metric
    return metrics.f1_score(true_target, prediction, average='macro')


def roc_auc(true_target, prediction_prob, target_levels):
    # ROC AUC for classification
    return metrics.roc_auc_score(true_target, prediction_prob,
                                 multi_class='ovo', labels=target_levels)


def get_num_validated(true_target, _):
    return len(true_target)


# The mapping from name to function as well as defining
# what gets passed in

metric_funcs = {'roc_auc': {'function': roc_auc,
                            'runs_on': 'prob'},
                'r2_score': {'function': r2_score,
                             'runs_on': 'pred'},
                'rms_score': {'function': rms_score,
                              'runs_on': 'pred'},
                'mad_score': {'function': mad_score,
                              'runs_on': 'pred'},
                'f1_score': {'function': f1_score,
                             'runs_on': 'pred'},
                'num_validated': {'function': get_num_validated,
                                  'runs_on': 'pred'}}


def get_metric(metric_name, true_target, prediction, pred_prob, target_levels):
    func = metric_funcs[metric_name]['function']
    runs_on = metric_funcs[metric_name]['runs_on']
    if runs_on == 'prob':
        metric = func(true_target, pred_prob, target_levels)
    elif runs_on == 'pred':
        metric = func(true_target, prediction)
    else:
        raise ValueError("Do not understand runs_on = %s" % runs_on)

    logger.info('%s : %s' % (metric_name, metric))
    return metric


def get_validation_metrics(metric_names, true_target, prediction, pred_prob, target_levels):
    assert len(true_target) > 0

    n_validated = len(true_target)
    logger.info('n_validated: %s' % n_validated)

    validation_metrics = {metric_name: get_metric(metric_name, true_target, prediction, pred_prob, target_levels)
                          for metric_name in metric_names}

    logger.info('Done validation metrics')

    return validation_metrics
