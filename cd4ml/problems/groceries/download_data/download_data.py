from cd4ml.filenames import get_problem_files
from cd4ml.utils.utils import download_to_file_from_url, shuffle_csv_file
import zipfile
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

download_params = {'key': 'store47-2016',
                   'gcs_bucket': 'raw/master',
                   'base_url': 'https://github.com/luizmachado/CDMLDataset'}


def get_grocery_url_and_files(problem_name):
    file_names = get_problem_files(problem_name)
    key = download_params['key']
    gcs_bucket = download_params['gcs_bucket']
    base_url = download_params['base_url']

    filename = file_names['raw_grocery_data']
    url = "%s/%s/%s.zip" % (base_url, gcs_bucket, key)
    filename_shuffled = file_names['grocery_data_shuffled']
    return url, filename, filename_shuffled


def download(problem_name, use_cache=True):
    url, filename, filename_shuffled = get_grocery_url_and_files(problem_name)
    zipname = f"{filename}.zip"
    download_to_file_from_url(url, zipname, use_cache=use_cache)
    target_dir = Path(filename).parent
    logger.inf(f"Unzipping: {zipname} @ {target_dir}")
    with zipfile.ZipFile(zipname, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    shuffle_csv_file(filename, filename_shuffled)
