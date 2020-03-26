from cd4ml.run_ml import run_all
from cd4ml.download_data import run_download_data


def download_data():
    print('Downloading data')
    run_download_data()
    print('Done downloading data')


def train_model():
    model_name = 'random_forest'
    print('Training Model')
    run_all(model_name=model_name, seed=8675309)
    print('Done training and validating model')
