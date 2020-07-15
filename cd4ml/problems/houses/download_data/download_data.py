from time import time
import os
import urllib
from cd4ml.filenames import file_names


def download_house_data(pipeline_params, use_cache=True):
    # The simulated house price data

    # Reduced in size to include only training data
    url = pipeline_params['problem_params']['download_data_info']['url']

    filename = file_names['raw_house_data']
    if not os.path.exists(filename) or not use_cache:
        print('Downloading house sale data')
        start = time()
        urllib.request.urlretrieve(url, filename)
        runtime = time()-start
        print('Download took %0.2f seconds' % runtime)
    else:
        print('Used cached file')
