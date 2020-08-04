from cd4ml.utils import get_git_hash, import_relative_module


def get_feature_set_class(problem_name, feature_set_name, this_file):
    """
    Get the FeatureSet class corresponding to the feature_set_name
    using relative paths
    :param problem_name: problem_name
    :param feature_set_name: feature set base filename
    :param this_file: __file__ from local scope of calling function
    :return: loaded module
    """
    module = import_relative_module(this_file, 'problems.%s.feature_sets' % problem_name, feature_set_name)
    feature_class = module.FeatureSet
    return feature_class


class Specification:
    def __init__(self,
                 problem_name,
                 feature_set_name,
                 ml_pipeline_params_name,
                 algorithm_name,
                 algorithm_params_name,
                 algorithm_name_actual):

        self.spec = {'problem_name': problem_name,
                     'feature_set_name': feature_set_name,
                     'ml_pipeline_params_name': ml_pipeline_params_name,
                     'algorithm_name': algorithm_name,
                     'algorithm_name_actual': algorithm_name_actual,
                     'algorithm_params_name': algorithm_params_name,
                     'git_hash': get_git_hash()}

    def problem_specification_name(self, with_git_hash=True):
        sep = "#"

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


def get_ml_pipeline_params(problem_name, ml_pipeline_params_name, this_file):
    module = import_relative_module(this_file, 'problems.%s.ml_pipelines' % problem_name, ml_pipeline_params_name)
    return module.ml_pipeline_params


def get_algorithm_params(this_file, problem_name, algorithm_name_actual, algorithm_params_name):
    path = 'problems.%s.algorithms.%s' % (problem_name, algorithm_name_actual)
    module = import_relative_module(this_file, path, algorithm_params_name)

    return module.model_parameters
