from cd4ml.run_ml_model import run_model
from cd4ml.download_data import run_download_data
from cd4ml.splitter import run_splitter


def download_data():
    print('Downloading data')
    run_download_data()
    print('Done downloading data')


def split_data():
    print('Splitting data')
    run_splitter()
    print('Done splitting data')


def train_model():
    model_name = 'random_forest'
    print('Training Model')
    run_model(model_name=model_name, seed=8675309)
    print('Done training model')
