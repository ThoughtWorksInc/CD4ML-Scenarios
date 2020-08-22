import logging
import mlflow
from cd4ml.utils.problem_utils import get_last_model_subdir
from cd4ml.filenames import get_model_files, get_problem_files
from cd4ml.utils.utils import get_json
from mlflow.tracking import MlflowClient


def get_message(model_id, metric_name, metric_value,
                threshold_min, threshold_max, accepted):

    if accepted:
        qualifier = ''
    else:
        qualifier = 'NOT '

    template = "Metric: {metric_name} for Model: {model_id} was {qualifier}accepted, " \
               "value: {metric_value}, " \
               "threshold_min: {threshold_min}, threshold_max: {threshold_max}"

    message = template.format(model_id=model_id,
                              metric_name=metric_name,
                              metric_value=metric_value,
                              threshold_min=threshold_min,
                              threshold_max=threshold_max,
                              qualifier=qualifier)
    return message


def modify_acceptance_flag(model_id, host_name, flag, registry_host_name):

    logger = logging.getLogger(__name__)
    mlflow.set_tracking_uri(uri=host_name)

    logger.info("Reporting acceptance data for model %s" % model_id)

    file_names = get_model_files(model_id)
    specification = get_json(file_names['model_specification'])

    mlflow.set_experiment(specification['problem_name'])

    client = MlflowClient(tracking_uri=registry_host_name)

    # this apparently does not work, run_id is not the model_id
    run_id = model_id
    client.set_tag(run_id, "DidPassAcceptanceTest", flag)


def is_model_accepted(model_id):
    model_files = get_model_files(model_id)
    spec_file = model_files['model_specification']
    specs = get_json(spec_file)
    problem_name = specs['problem_name']

    problem_files = get_problem_files(problem_name)
    params = get_json(problem_files['acceptance_params'])

    metric_name = params['acceptance_metric']
    threshold_min = params['acceptance_threshold_min']
    threshold_max = params['acceptance_threshold_max']

    metrics = get_json(model_files['model_metrics'])
    metric_value = metrics[metric_name]

    accepted = threshold_min <= metric_value <= threshold_max

    message = get_message(model_id, metric_name, metric_value,
                          threshold_min, threshold_max, accepted)

    return accepted, message


def main(*args):
    """
    Check model meets acceptance threshold
    """
    args = args[0]

    logger = logging.getLogger(__name__)

    if len(args) > 0:
        registry_host_name = args[0]
    else:
        # for the local environment only, Jenkins will give the
        # relevant url
        registry_host_name = "http://localhost:12000"

    if len(args) > 1:
        model_id = args[1]
    else:
        latest_subdir = get_last_model_subdir()
        if latest_subdir is None:
            raise IOError('No models found')

        model_id = latest_subdir.split('/')[-1]

    accepted, message = is_model_accepted(model_id)

    if not accepted:
        modify_acceptance_flag(model_id, registry_host_name, 'no', registry_host_name)
        raise ValueError(message)
    else:
        modify_acceptance_flag(model_id, registry_host_name, 'yes', registry_host_name)
        logger.info(message)
