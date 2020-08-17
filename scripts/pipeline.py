import numpy as np
import logging

from cd4ml.problems import get_problem

DEFAULT_ARGUMENT = 'default'


def main(*args):
    """
    Run the pipeline
    """
    logger = logging.getLogger(__name__)
    args = args[0]
    problem_name = args[0]
    np.random.seed(462748)

    logger.info('Problem name desired: {}'.format(problem_name))

    if len(args) > 1:
        ml_pipeline_params_name = args[1]
    else:
        ml_pipeline_params_name = DEFAULT_ARGUMENT

    if len(args) > 2:
        feature_set_name = args[2]
    else:
        feature_set_name = DEFAULT_ARGUMENT

    if len(args) > 3:
        algorithm_name = args[3]
    else:
        algorithm_name = DEFAULT_ARGUMENT

    if len(args) > 4:
        algorithm_params_name = args[4]
    else:
        algorithm_params_name = DEFAULT_ARGUMENT

    # TODO: Allow a different data_downloader

    problem = get_problem(problem_name,
                          data_downloader='default',
                          ml_pipeline_params_name=ml_pipeline_params_name,
                          feature_set_name=feature_set_name,
                          algorithm_name=algorithm_name,
                          algorithm_params_name=algorithm_params_name)

    # Call the run_all method, which will perform the entire data pipeline
    problem.run_all()

