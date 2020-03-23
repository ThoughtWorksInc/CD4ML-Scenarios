import os
import urllib.request
import argparse
import zipfile
from cd4ml.filenames import file_names, data_raw, data_source


def load_data(path, key):
    gcsBucket = "continuous-intelligence"

    if not os.path.exists(os.path.join(path, key)):
        url = "https://storage.googleapis.com/%s/%s" % (gcsBucket, key)
        urllib.request.urlretrieve(url, os.path.join(path, key))


def main():
    key = 'store47-2016.csv'
    load_data(data_raw, key)
    # zip_ref = zipfile.ZipFile(file_names['zipped_data'], 'r')
    # zip_ref.extractall(data_raw)

    print("Finished unzipping data")


def main_dep():
    parser = argparse.ArgumentParser(description='Download files from Google Storage.')
    parser.add_argument('--model', action='store_true', default=False, help='Downloads model (data/decision_tree/model.pkl) instead of input file (data/raw/store47-2016.csv)')
    args = parser.parse_args()
    
    with zipfile.ZipFile('data/source/store47-2016.csv.zip', 'r') as zip_ref:
        zip_ref.extractall('data/raw')
    
    # if args.model:
    #     print("Loading model...")
    #     load_data(path='data/decision_tree', key='model.pkl')
    # else:
    #     print("Loading input data...")
    #     load_data(path='data/raw', key='store47-2016.csv')
    print("Finished unzipping data")


if __name__ == "__main__":
    main()
