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

    ph.download_data(problem_name)
    ph.train_and_validate_model(problem_name)
