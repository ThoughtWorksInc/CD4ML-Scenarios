from cd4ml.decision_tree import main
from cd4ml.download_data import main as main_download


def download_data():
    print('Downloading data')
    main_download()
    print('Done downloading data')


def run_simple_model():
    print('Run Simple Model')
    main(seed=8675309)
    print('Done running model')
