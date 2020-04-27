from time import time
import os
import zipfile
import urllib
from cd4ml.filenames import data_raw, file_names


def download_zillow_data(pipeline_params, use_cache=True):
    # The Zillow home price challenge
    # Originally from here https://www.kaggle.com/c/zillow-prize-1

    # Reduced in size to include only training data
    url = pipeline_params['problem_params']['download_data_info']['url']

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
