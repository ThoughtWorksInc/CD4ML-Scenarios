from time import time
from cd4ml.problems.shopping.download_data.download_data import download_shopping_data
from cd4ml.problems.zillow.download_data.download_data import download_zillow_data


def run_download_data(pipeline_params, use_cache=True):
    start = time()

    problem = pipeline_params['problem_name']
    if problem == 'shopping':
        download_shopping_data(pipeline_params, use_cache=use_cache)
    elif problem == 'zillow':
        download_zillow_data(pipeline_params, use_cache=use_cache)
    else:
        raise ValueError('Do not know problem: %s' % problem)

    runtime = time() - start
    print('Download time: %0.1f seconds' % runtime)
