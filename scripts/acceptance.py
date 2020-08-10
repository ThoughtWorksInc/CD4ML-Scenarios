from cd4ml.accept_model import check_model_performance


def main(*args):
    """
    Check model meets acceptance threshold
    """
    problem = get_problem()
    pipeline_params = problem.pipeline_params

    metric = pipeline_params['acceptance_metric']
    threshold_min = pipeline_params['acceptance_threshold_min']
    threshold_max = pipeline_params['acceptance_threshold_max']

    check_model_performance(metric, threshold_min, threshold_max)
