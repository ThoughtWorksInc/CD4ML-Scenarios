import datetime
import os
from pathlib import Path

from cd4ml.filenames import get_model_files
from scripts import acceptance as acceptance_script


def test_acceptance_with_model_id():
    model_id = acceptance_script.parse_arguments(['my_test_model_id'])
    assert model_id == 'my_test_model_id'


earlier_time = int(datetime.datetime(2020, 8, 29, 12, 0, 0).timestamp())
later_time = int(datetime.datetime(2020, 8, 29, 14, 0, 0).timestamp())


def test_acceptance_with_no_arguments(tmp_path):
    os.environ["CD4ML_DATA_DIR"] = str(tmp_path)
    files = get_model_files('', base_data_dir=tmp_path)

    base_results_directory = files['results_folder']
    earlier_folder = Path(base_results_directory, "earlier")
    earlier_folder.mkdir(parents=True)
    os.utime(earlier_folder, (earlier_time, earlier_time))
    latest_folder = Path(base_results_directory, "later")
    latest_folder.mkdir(parents=True)
    os.utime(earlier_folder, (later_time, later_time))

    model_id = acceptance_script.parse_arguments([])
    del os.environ["CD4ML_DATA_DIR"]

    assert model_id == 'later'
