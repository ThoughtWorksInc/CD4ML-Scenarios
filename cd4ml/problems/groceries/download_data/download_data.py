import os
from cd4ml.utils import download_to_file_from_url, shuffle_csv_file
from cd4ml.filenames import get_filenames


def get_grocery_url_and_files(pipeline_params):
    file_names = get_filenames(pipeline_params['problem_name'])
    path = file_names['raw_data_dir']
    data_info = pipeline_params['problem_params']['download_data_info']
    key = data_info['key']
    gcs_bucket = data_info['gcs_bucket']
    base_url = data_info['base_url']

    filename = os.path.join(path, key)
    url = "%s/%s/%s" % (base_url, gcs_bucket, key)
    filename_shuffled = filename.replace('.csv', '.shuffled.csv')

    return url, filename, filename_shuffled


def download_grocery_data(pipeline_params, use_cache=True):
    url, filename, filename_shuffled = get_grocery_url_and_files(pipeline_params)
    download_to_file_from_url(url, filename, use_cache=use_cache)
    shuffle_csv_file(filename, filename_shuffled)
