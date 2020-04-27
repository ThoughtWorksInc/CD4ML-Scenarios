import os
import urllib.request
from time import time
import zipfile
from cd4ml.filenames import data_raw, file_names


def run_download_data(pipeline_params, use_cache=True):
    problem = pipeline_params['problem']
    if problem == 'shopping':
        download_shopping_data(pipeline_params, use_cache=use_cache)
    elif problem == 'zillow':
        download_zillow_data(pipeline_params, use_cache=use_cache)
    else:
        raise ValueError('Do not know problem: %s' % problem)


def download_shopping_data(pipeline_params, use_cache=True):
    path = data_raw
    data_info = pipeline_params['download_data_info']

    key = data_info['key']
    gcs_bucket = data_info['gcs_bucket']
    base_url = data_info['base_url']

    filename = os.path.join(path, key)

    if not os.path.exists(filename) or not use_cache:
        url = "%s/%s/%s" % (base_url, gcs_bucket, key)
        urllib.request.urlretrieve(url, filename)

    else:
        print('Used cached file')


def download_zillow_data(pipeline_params, use_cache=True):
    # The Zillow home price challenge
    # From here https://www.kaggle.com/c/zillow-prize-1

    # Only training data properties here
    url = "https://github.com/dave31415/zillow_data_small/archive/master.zip"
    # faster, takes about 15 seconds

    filename = file_names['raw_zillow_data']
    if not os.path.exists(filename) or not use_cache:
        print('Downloading Zillow data')
        start = time()
        urllib.request.urlretrieve(url, filename)
        runtime = time()-start
        print('Download took %0.2f seconds' % runtime)
    else:
        print('Used cached file')

    unpack_zillow()


def unpack_zillow():
    filename = file_names['raw_zillow_data']
    print('unzipping zillow data')
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(data_raw)
