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


if __name__ == "__main__":
    main()
