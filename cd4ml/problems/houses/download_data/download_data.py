from time import time
import os
import urllib
from cd4ml.filenames import file_names


def url_to_file(url, filename, use_cache=True):
    if not os.path.exists(filename) or not use_cache:
        print('House data file download from url: %s' % url)
        start = time()
        urllib.request.urlretrieve(url, filename)
        runtime = time()-start
        print('Download took %0.2f seconds' % runtime)
    else:
        print('Used cached file')


def download_house_data(pipeline_params, use_cache=True):
    # The simulated house price data

    url = pipeline_params['problem_params']['download_data_info']['url']
    filename = file_names['raw_house_data']
    url_to_file(url, filename, use_cache=use_cache)

    url = pipeline_params['problem_params']['download_data_info']['url_lookup']
    filename = file_names['house_data_zip_lookup']
    url_to_file(url, filename, use_cache=use_cache)
