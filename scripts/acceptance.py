import argparse
import logging

from cd4ml.exceptions.ModelNotAcceptedError import ModelNotAcceptedError
from cd4ml.filenames import get_model_files
from cd4ml.utils.utils import get_json
from scripts.common_arg_parsers import get_model_id_location


def get_message(model_id, metric_name, metric_value,
                threshold_min, threshold_max, accepted):
    qualifier = '' if accepted else 'NOT '
    message = f"Metric: {metric_name} for Model: {model_id} was {qualifier}accepted, " \
              f"value: {metric_value}, " \
              f"threshold_min: {threshold_min}, threshold_max: {threshold_max}"
    return message


def is_model_accepted(model_id):
    model_files = get_model_files(model_id)
    params = get_json(model_files['ml_pipeline_params'])

    metric_name = params['acceptance_metric'].replace("'", "")
    threshold_min = float(params['acceptance_threshold_min'])
    threshold_max = float(params['acceptance_threshold_max'])

    metrics = get_json(model_files['model_metrics'])
    metric_value = metrics[metric_name]

    accepted = threshold_min <= metric_value <= threshold_max

    message = get_message(model_id, metric_name, metric_value,
                          threshold_min, threshold_max, accepted)

    return accepted, message


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model_id",
                        help="The model_id folder to use to report",
                        nargs='?',
                        default=None)

    parsed_args = parser.parse_args(args)
    model_id = get_model_id_location(parsed_args.model_id)

    return model_id


def main(args):
    """
    Check model meets acceptance threshold
    """
    logger = logging.getLogger(__name__)
    model_id = parse_arguments(args)
    accepted, message = is_model_accepted(model_id)

    if not accepted:
        logger.error(message)
        raise ModelNotAcceptedError(message)
    else:
        logger.info(message)
