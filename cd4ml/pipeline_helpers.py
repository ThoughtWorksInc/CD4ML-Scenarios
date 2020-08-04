from cd4ml.download_data import run_download_data
from cd4ml.get_problem import get_problem


def download_data(problem_name):
    print('Downloading data')
    run_download_data(problem_name)
    print('Done downloading data')


def train_and_validate_model(problem_name,
                             ml_pipeline_params_name='default',
                             feature_set_name='default',
                             algorithm_name='default',
                             algorithm_params_name='default'):

    print('Training and validating model')
    problem = get_problem(problem_name,
                          ml_pipeline_params_name=ml_pipeline_params_name,
                          feature_set_name=feature_set_name,
                          algorithm_name=algorithm_name,
                          algorithm_params_name=algorithm_params_name)

    problem.run_all()
    print('Done training and validating model')
