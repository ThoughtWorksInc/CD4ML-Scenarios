"""
Keep all filename/path logic here rather than hardcoded paths all over the code
"""
import os

from cd4ml.utils.utils import ensure_dir_exists


def get_filenames(problem_name, problem_specification_name='not-specified'):
    base_directory = os.getenv('CD4ML_DATA_DIR', 'data')
    base_directory = os.path.realpath(base_directory)

    ensure_dir_exists(base_directory)

    _raw_data_dir = "%s/{problem_name}/raw_data" % base_directory
    _results_dir = "%s/results/{problem_specification_name}" % base_directory

    _file_names = {
        'metrics': '%s/metrics.json' % _results_dir,
        'parameters': '%s/parameters.json' % _results_dir,
        'raw_grocery_data': '%s/groceries.csv' % _raw_data_dir,
        'grocery_data_shuffled': '%s/groceries_shuffled.csv' % _raw_data_dir,
        'full_model': '%s/full_model.pkl' % _results_dir,
        'full_model_deployed': '%s/full_model_deployed.pkl' % _results_dir,
        'encoder': '%s/encoder.json' % _results_dir,
        'validation_plot': '%s/validation_plot.html' % _results_dir,
        'raw_house_data': '%s/house_sales.csv' % _raw_data_dir,
        'house_data_zip_lookup': '%s/zip_lookup.csv' % _raw_data_dir,
        'iris_data': '%s/iris.csv' % _raw_data_dir
    }

    file_names = {k: v.format(problem_name=problem_name,
                              problem_specification_name=problem_specification_name)
                  for k, v in _file_names.items()}

    raw_data_dir = _raw_data_dir.format(problem_name=problem_name)
    results_dir = _results_dir.format(problem_specification_name=problem_specification_name)

    ensure_dir_exists(raw_data_dir)
    if 'not-specified' not in results_dir:
        ensure_dir_exists(results_dir)

    file_names['raw_data_dir'] = raw_data_dir
    file_names['results_dir'] = results_dir
    file_names['model_cache_dir'] = "{data_dir}/cache/{problem_name}/{problem_specification_name}"\
        .format(data_dir=base_directory,
                problem_name=problem_name,
                problem_specification_name=problem_specification_name)

    return file_names
