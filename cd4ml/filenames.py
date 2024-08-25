"""
    Keep all filename/path logic here rather than hardcoded paths all over the code
"""
import os
from cd4ml.utils.utils import ensure_dir_exists

this_dir = os.path.dirname(__file__)
root_dir = os.path.realpath(this_dir + "/..")

_default_data_dir = "%s/%s" % (root_dir, 'data')

_model_file_name = "full_model.pkl"


def _get_base_dirs(base_data_dir=None):
    # makes a fresh call to environment for variable each call
    if base_data_dir is None:
        base_data_directory = os.getenv('CD4ML_DATA_DIR', _default_data_dir)
    else:
        base_data_directory = base_data_dir

    ensure_dir_exists(base_data_directory)

    raw_base_dir = "%s/%s" % (base_data_directory, 'raw_data')
    model_results_base_dir = "%s/%s" % (base_data_directory, 'results')

    raw_problem_data_dir = "%s/{problem_name}" % raw_base_dir
    model_results_dir = "%s/{model_id}" % model_results_base_dir

    model_cache_dir = "%s/%s" % (base_data_directory, 'cache')
    ensure_dir_exists(model_cache_dir)

    return raw_problem_data_dir, model_results_dir, model_cache_dir


def _get_model_file_templates(model_results_dir):
    # TODO: do we really need encoder cacheing?
    file_names_model = {
        'model_metrics': '%s/model_metrics.json' % model_results_dir,
        'model_specification': '%s/model_specification.json' % model_results_dir,
        'ml_pipeline_params': '%s/ml_pipeline_params.json' % model_results_dir,
        'encoder': '%s/encoder.json' % model_results_dir,
        'full_model': '%s/%s' % (model_results_dir, _model_file_name),
        'validation_plot': '%s/validation_plot.html' % model_results_dir,
        'results_folder': model_results_dir
    }

    return file_names_model


def _get_problem_file_templates(raw_problem_data_dir):
    file_names_problem = {
        'groceries': {
            'raw_grocery_data': '%s/store47-2016.csv' % raw_problem_data_dir,
            'grocery_data_shuffled': '%s/store47-2016_shuffled.csv' % raw_problem_data_dir
        },
        'houses': {
            'raw_house_data': '%s/house_sales.csv' % raw_problem_data_dir,
            'house_data_zip_lookup': '%s/zip_lookup.csv' % raw_problem_data_dir
        },
        'iris': {
            'raw_iris_data': '%s/iris.csv' % raw_problem_data_dir
        }
    }

    return file_names_problem


def get_model_files(model_id, base_data_dir=None):
    """
    Gets a dictionary of all output files related to a model
    :param model_id: the unique model id string
    :param base_data_dir: base data dir, mostly for testing and experimentation
        default is to use environment variable or default value above
    :return: dictionary of relevant full-path file names
    """
    _, model_results_dir, __ = _get_base_dirs(base_data_dir)
    model_file_templates = _get_model_file_templates(model_results_dir)
    ensure_dir_exists(model_file_templates['results_folder'].format(model_id=model_id))

    return {k: v.format(model_id=model_id) for k, v in model_file_templates.items()}


def get_problem_files(problem_name, base_data_dir=None):
    """
    Gets a dictionary of all input files related to a problem
    :param problem_name:  problem name string
    :param base_data_dir: base data dir, mostly for testing and experimentation
        default is to use environment variable or default value above
    :return: dictionary of relevant full-path file names
    """
    raw_problem_data_dir, _, __ = _get_base_dirs(base_data_dir)
    problem_file_templates = _get_problem_file_templates(raw_problem_data_dir)

    ensure_dir_exists(raw_problem_data_dir.format(problem_name=problem_name))

    problem_files = problem_file_templates[problem_name]
    return {k: v.format(problem_name=problem_name) for k, v in problem_files.items()}


def get_model_cache_file(problem_name, model_id, base_data_dir=None):
    """
    Get the model cache file
    :param problem_name: the problem name string
    :param model_id: the model id string
    :param base_data_dir: base data dir, mostly for testing and experimentation
        default is to use environment variable or default value above
    :return: model cache file
    """
    raw_problem_data_dir, _, model_cache_dir = _get_base_dirs(base_data_dir)

    return "{model_cache_dir}/{problem_name}/{model_id}/{model_file_name}" \
        .format(model_cache_dir=model_cache_dir,
                problem_name=problem_name,
                model_id=model_id,
                model_file_name=_model_file_name)
