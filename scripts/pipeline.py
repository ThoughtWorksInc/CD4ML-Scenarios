import numpy as np
from cd4ml import pipeline_helpers as ph


def main(*args):
    """
    Run the pipeline
    """
    args = args[0]
    problem_name = args[0]
    np.random.seed(462748)

    print('Problem name desired: %s' % problem_name)

    if len(args) > 1:
        ml_pipeline_params_name = args[1]
    else:
        ml_pipeline_params_name = 'default'

    if len(args) > 2:
        feature_set_name = args[2]
    else:
        feature_set_name = 'default'

    if len(args) > 3:
        algorithm_name = args[3]
    else:
        algorithm_name = 'default'

    if len(args) > 4:
        algorithm_params_name = args[4]
    else:
        algorithm_params_name = 'default'

    ph.download_data(problem_name)

    ph.train_and_validate_model(problem_name,
                                feature_set_name=feature_set_name,
                                ml_pipeline_params_name=ml_pipeline_params_name,
                                algorithm_name=algorithm_name,
                                algorithm_params_name=algorithm_params_name)
