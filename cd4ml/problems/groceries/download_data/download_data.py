from cd4ml.utils import download_to_file_from_url, shuffle_csv_file
from cd4ml.filenames import get_filenames

download_params = {'key': 'store47-2016.csv',
                   'gcs_bucket': 'continuous-intelligence',
                   'base_url': 'https://storage.googleapis.com'}


def get_grocery_url_and_files(problem_name):
    file_names = get_filenames(problem_name)
    key = download_params['key']
    gcs_bucket = download_params['gcs_bucket']
    base_url = download_params['base_url']

    filename = file_names['raw_grocery_data']
    url = "%s/%s/%s" % (base_url, gcs_bucket, key)
    filename_shuffled = file_names['grocery_data_shuffled']
    return url, filename, filename_shuffled


def download(problem_name, use_cache=True):
    url, filename, filename_shuffled = get_grocery_url_and_files(problem_name)
    download_to_file_from_url(url, filename, use_cache=use_cache)
    shuffle_csv_file(filename, filename_shuffled)
