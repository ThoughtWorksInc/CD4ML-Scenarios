from time import time
from cd4ml.problems.groceries.download_data.download_data import download_grocery_data
from cd4ml.problems.houses.download_data.download_data import download_house_data


def run_download_data(pipeline_params, use_cache=True):
    start = time()

    problem = pipeline_params['problem_name']
    if problem == 'groceries':
        download_grocery_data(pipeline_params, use_cache=use_cache)
    elif problem == 'houses':
        download_house_data(pipeline_params, use_cache=use_cache)
    else:
        raise ValueError('Do not know problem: %s' % problem)

    runtime = time() - start
    print('Download time: %0.1f seconds' % runtime)
