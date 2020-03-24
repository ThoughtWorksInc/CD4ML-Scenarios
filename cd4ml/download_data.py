import os
import urllib.request
from cd4ml.filenames import data_raw


def run_download_data():
    key = 'store47-2016.csv'
    path = data_raw
    gcs_bucket = "continuous-intelligence"

    if not os.path.exists(os.path.join(path, key)):
        url = "https://storage.googleapis.com/%s/%s" % (gcs_bucket, key)
        filename = os.path.join(path, key)
        urllib.request.urlretrieve(url, filename)
