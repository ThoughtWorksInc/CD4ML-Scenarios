from cd4ml.filenames import get_filenames
from cd4ml.utils.utils import download_to_file_from_url

download_params = {
                    'url': "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/"
                           "raw/639388c2cbc2120a14dcf466e85730eb8be498bb/iris.csv"
                   }


def download(use_cache=True):
    # The famous iris data
    url = download_params['url']
    file_names = get_filenames("iris")
    filename = file_names['iris_data']

    download_to_file_from_url(url, filename, use_cache=use_cache)
