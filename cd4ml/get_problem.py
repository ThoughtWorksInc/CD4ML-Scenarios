# parameters for running the pipeline
import yaml
from cd4ml.filenames import config_file
from cd4ml.utils import import_relative_module


def get_pipeline_params(problem_name,
                        problem_params_name,
                        ml_params_name,
                        algorithm_name,
                        this_file):

    problem_string = ":".join([problem_name, problem_params_name, ml_params_name, algorithm_name])

    if problem_params_name == 'default':
        problem_params_name = 'problem_params'
    if ml_params_name == 'default':
        ml_params_name = 'ml_model_params'

    problem_params = get_problem_params(problem_params_name, this_file)
    ml_params_all = get_ml_params(ml_params_name, this_file)

    if algorithm_name != 'default':
        problem_params['model_name'] = algorithm_name

    return {'problem_string': problem_string,
            'problem_name': problem_name,
            'problem_params': problem_params,
            'model_params': ml_params_all[problem_params['model_name']]}


def get_pipeline_config_deprecated_():
    filename = config_file
    return yaml.safe_load(open(filename, 'r'))


def get_problem_params(problem_params_file, this_file):
    """
    Get the problem params corresponding to the problem_params_file
    using relative paths
    :param problem_params_file: problem_params filename
    :param this_file: __file__ from local scope of calling function
    :return: loaded module
    """
    module = import_relative_module(this_file, 'config.problem_params', problem_params_file)
    return module.problem_params


def get_ml_params(ml_params_file, this_file):
    """
    Get the m params corresponding to the problem_params_file
    using relative paths
    :param ml_params_file: problem_params filename
    :param this_file: __file__ from local scope of calling function
    :return: loaded module
    """
    module = import_relative_module(this_file, 'config.ml_model_params', ml_params_file)
    return module.model_parameters


def get_problem(problem_name,
                ml_pipeline_params_name='default',
                feature_set_name='default',
                algorithm_name='default',
                algorithm_params_name='default'):

    Problem = import_relative_module(__file__, 'problems.' + problem_name, 'problem').Problem

    return Problem(problem_name,
                   ml_pipeline_params_name=ml_pipeline_params_name,
                   feature_set_name=feature_set_name,
                   algorithm_name=algorithm_name,
                   algorithm_params_name=algorithm_params_name)
