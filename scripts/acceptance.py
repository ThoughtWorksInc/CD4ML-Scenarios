from cd4ml.accept_model import check_model_performance
from cd4ml.pipeline_params import pipeline_params


def main(*args):
    """
    Check model meets acceptance threshold
    """
    metric = pipeline_params['acceptance_metric']
    threshold = pipeline_params['acceptance_threshold']
    check_model_performance(metric, threshold)
