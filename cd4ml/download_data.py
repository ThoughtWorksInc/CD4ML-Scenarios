from time import time
from cd4ml.utils import import_relative_module


def run_download_data(problem_name, use_cache=True):
    start = time()

    module = import_relative_module(__file__,
                                    'problems.%s.download_data' % problem_name,
                                    'download_data')
    download = module.download

    download(problem_name, use_cache=use_cache)

    runtime = time() - start
    print('Download time: %0.1f seconds' % runtime)
