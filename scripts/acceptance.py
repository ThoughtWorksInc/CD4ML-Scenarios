from cd4ml.accept_model import check_model_performance
from cd4ml.utils.problem_utils import get_last_model_subdir

# TODO: finish


def main(*args):
    """
    Check model meets acceptance threshold
    """
    return
    args = args[0]

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

    metric = pipeline_params['acceptance_metric']
    threshold_min = pipeline_params['acceptance_threshold_min']
    threshold_max = pipeline_params['acceptance_threshold_max']

    check_model_performance(metric, threshold_min, threshold_max)
