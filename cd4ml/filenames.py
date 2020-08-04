"""
Keep all filename/path logic here rather than polluting code with hardcoded paths
"""
import os
from cd4ml.utils import ensure_dir_exists

module_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = "%s/%s" % (module_dir, 'config')
config_file = "%s/%s" % (config_dir, 'pipeline_config.yaml')

template_dir = "%s/%s" % (module_dir, 'webapp/templates')

data_dir_default = 'data'
data_dir = os.getenv('CD4ML_DATA_DIR', data_dir_default)
data_dir = os.path.realpath(data_dir)

_raw_data_dir = "%s/{problem_name}/raw_data" % data_dir
_results_dir = "%s/results/{problem_specification_name}" % data_dir

ensure_dir_exists(data_dir)


_file_names = {
    'metrics': '%s/metrics.json' % _results_dir,
    'raw_grocery_data': '%s/groceries.csv' % _raw_data_dir,
    'grocery_data_shuffled': '%s/groceries_shuffled.csv' % _raw_data_dir,
    'full_model': '%s/full_model.pkl' % _results_dir,
    'full_model_deployed': '%s/full_model_deployed.pkl' % _results_dir,
    'ml_params': 'ml_model_params.py',
    'encoder': '%s/encoder.json' % _results_dir,
    'validation_plot': '%s/validation_plot.html' % _results_dir,
    'raw_house_data': '%s/house_sales.csv' % _raw_data_dir,
    'house_data_zip_lookup': '%s/zip_lookup.csv' % _raw_data_dir,
    'pipeline_config': "%s/%s" % (config_dir, 'pipeline_config.yaml'),
    'dynamic_index': "%s/%s" % (template_dir, 'index_dynamic.html'),
    'index_models': "%s/%s" % (template_dir, 'index_models.html')
}


def get_filenames(problem_name, problem_specification_name='not-specified'):
    assert isinstance(problem_name, str)

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

    return file_names
