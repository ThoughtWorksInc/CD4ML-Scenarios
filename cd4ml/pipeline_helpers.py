from cd4ml.decision_tree import main
from cd4ml.download_data import main as main_download
from cd4ml.splitter import main as main_splitter


def download_data():
    print('Downloading data')
    main_download()
    print('Done downloading data')


def split_data():
    print('Splitting data')
    main_splitter()
    print('Done splitting data')


def train_model():
    print('Training Model')
    main(seed=8675309)
    print('Done training model')
