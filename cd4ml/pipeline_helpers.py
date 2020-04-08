from cd4ml.run_ml import run_all
from cd4ml.download_data import run_download_data


def download_data(pipeline_params):
    print('Downloading data')
    run_download_data(pipeline_params)
    print('Done downloading data')


def train_and_validate_model(pipeline_params):
    print('Training and validating model')
    run_all(pipeline_params)
    print('Done training and validating model')
