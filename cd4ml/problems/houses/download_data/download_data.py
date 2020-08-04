from cd4ml.filenames import get_filenames
from cd4ml.utils import download_to_file_from_url

download_params = {
                    'url': "https://github.com/dave31415/house_price/raw/master/data/house_data_100000.csv",
                    'url_lookup': "https://github.com/dave31415/house_price/raw/master/data/zip_lookup.csv"
                   }


def download(problem_name, use_cache=True):
    # The simulated house price data
    url = download_params['url']
    file_names = get_filenames(problem_name)
    filename = file_names['raw_house_data']

    download_to_file_from_url(url, filename, use_cache=use_cache)

    url = download_params['url_lookup']
    filename = file_names['house_data_zip_lookup']
    download_to_file_from_url(url, filename, use_cache=use_cache)
