from cd4ml.filenames import get_problem_files
from cd4ml.utils.utils import download_to_file_from_url

download_params = {
                    'url': "https://github.com/luizmachado/CD4ML/raw/master/dataset/iris.csv"
                   }


def download(use_cache=False):
    # The simulated house price data
    url = download_params['url']
    file_names = get_problem_files("iris")
    filename = file_names['raw_iris_data']

    download_to_file_from_url(url, filename, use_cache=use_cache)
