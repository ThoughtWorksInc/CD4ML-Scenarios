from cd4ml.filenames import get_problem_files
from cd4ml.utils.utils import download_to_file_from_url

download_params = {
                    'url': "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/"
                           "raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
                   }


def download(use_cache=False):
    # The simulated house price data
    url = download_params['url']
    file_names = get_problem_files("iris")
    filename = file_names['raw_iris_data']

    download_to_file_from_url(url, filename, use_cache=use_cache)
