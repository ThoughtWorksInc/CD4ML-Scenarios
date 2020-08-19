import os
from cd4ml.filenames import get_model_files


class Specification:
    def __init__(self,
                 problem_name,
                 data_downloader,
                 ml_pipeline_params_name,
                 feature_set_name,
                 algorithm_name,
                 algorithm_params_name,
                 algorithm_name_actual):

        self.spec = {'problem_name': problem_name,
                     'data_downloader': data_downloader,
                     'ml_pipeline_params_name': ml_pipeline_params_name,
                     'feature_set_name': feature_set_name,
                     'algorithm_name': algorithm_name,
                     'algorithm_name_actual': algorithm_name_actual,
                     'algorithm_params_name': algorithm_params_name,
                     'git_hash': "NOTIMPLEMENTED"}

    def problem_specification_name(self, with_git_hash=False):
        sep = "$"

        parts = ['{problem_name}',
                 '{ml_pipeline_params_name}',
                 '{feature_set_name}',
                 '{algorithm_name}',
                 '{algorithm_params_name}']

        template = sep.join(parts)
        string = template.format(**self.spec)
        if with_git_hash:
            string = string + '#' + self.spec['git_hash']

        return string


def get_subdirs(results_dir):
    results = [os.path.join(results_dir, d) for d in os.listdir(results_dir)]
    return [d for d in results if os.path.isdir(d)]


def get_last_model_subdir():
    # use empty string to get the root model_results_dir
    file_names = get_model_files('')

    results_dir = file_names['results_folder']
    subdirs = get_subdirs(results_dir)
    if len(subdirs) == 0:
        return None

    latest_subdir = max(subdirs, key=os.path.getmtime)
    return latest_subdir
