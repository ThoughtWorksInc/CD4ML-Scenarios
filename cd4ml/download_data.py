import os
import urllib.request
from cd4ml.filenames import data_raw


def run_download_data(pipeline_params):
    path = data_raw
    data_info = pipeline_params['download_data_info']

    key = data_info['key']
    gcs_bucket = data_info['gcs_bucket']
    base_url = data_info['base_url']

    if not os.path.exists(os.path.join(path, key)):
        url = "%s/%s/%s" % (base_url, gcs_bucket, key)
        filename = os.path.join(path, key)
        urllib.request.urlretrieve(url, filename)
