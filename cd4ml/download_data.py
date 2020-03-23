import os
import urllib.request
from cd4ml.filenames import data_raw


def run_download_data():
    key = 'store47-2016.csv'
    path = data_raw
    gcsBucket = "continuous-intelligence"

    if not os.path.exists(os.path.join(path, key)):
        url = "https://storage.googleapis.com/%s/%s" % (gcsBucket, key)
        urllib.request.urlretrieve(url, os.path.join(path, key))
