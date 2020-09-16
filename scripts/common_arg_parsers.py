import argparse
import logging

from cd4ml.filenames import get_model_files
from cd4ml.utils.problem_utils import get_last_model_subdir


def get_model_id_location(model_id_arg):
    logger = logging.getLogger(__name__)
    if model_id_arg is None:
        latest_subdir = get_last_model_subdir()
        if latest_subdir is None:
            results_dir = get_model_files('')['results_dir']
            raise IOError(f'No models found in {results_dir}')

        model_id = latest_subdir.split('/')[-1]
        logger.info(f"Using model_id {model_id}")
    else:
        model_id = model_id_arg

    return model_id
