import os
import urllib.request
from cd4ml.filenames import data_raw


def download_shopping_data(pipeline_params, use_cache=True):
    path = data_raw
    data_info = pipeline_params['problem_params']['download_data_info']

    key = data_info['key']
    gcs_bucket = data_info['gcs_bucket']
    base_url = data_info['base_url']

    filename = os.path.join(path, key)

    if not os.path.exists(filename) or not use_cache:
        url = "%s/%s/%s" % (base_url, gcs_bucket, key)
        urllib.request.urlretrieve(url, filename)

    else:
        print('Used cached file')
