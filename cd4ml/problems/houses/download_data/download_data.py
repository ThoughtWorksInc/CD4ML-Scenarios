from cd4ml.filenames import get_filenames
from cd4ml.utils import download_to_file_from_url


def download_house_data(pipeline_params, use_cache=True):
    # The simulated house price data
    file_names = get_filenames(pipeline_params['problem_name'])

    url = pipeline_params['problem_params']['download_data_info']['url']
    filename = file_names['raw_house_data']
    download_to_file_from_url(url, filename, use_cache=use_cache)

    url = pipeline_params['problem_params']['download_data_info']['url_lookup']
    filename = file_names['house_data_zip_lookup']
    download_to_file_from_url(url, filename, use_cache=use_cache)
