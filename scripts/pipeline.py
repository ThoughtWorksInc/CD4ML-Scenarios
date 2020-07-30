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
        feature_set_name = args[1]
    else:
        feature_set_name = 'default'

    ph.download_data(problem_name)
    ph.train_and_validate_model(problem_name, feature_set_name)
