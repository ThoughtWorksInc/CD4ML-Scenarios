from cd4ml.download_data import run_download_data
from cd4ml.get_problem import get_problem


def download_data(problem_name):
    print('Downloading data')
    problem = get_problem(problem_name)
    run_download_data(problem.pipeline_params)
    print('Done downloading data')


def train_and_validate_model(problem_name,
                             feature_set_name='default',
                             problem_params_name='default',
                             ml_params_name='default',
                             algorithm_name='default'):

    print('Training and validating model')
    problem = get_problem(problem_name,
                          feature_set_name=feature_set_name,
                          problem_params_name=problem_params_name,
                          ml_params_name=ml_params_name,
                          algorithm_name=algorithm_name)

    print(problem.pipeline_params)

    problem.run_all()
    print('Done training and validating model')
