"""
Keep all filename/path logic here rather than polluting code with hardcoded paths
"""
import os
from cd4ml.utils import ensure_dir_exists

module_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = "%s/%s" % (module_dir, 'config')
template_dir = "%s/%s" % (module_dir, 'webapp/templates')

data_dir_default = 'data'
data_dir = os.getenv('CD4ML_DATA_DIR', data_dir_default)
data_dir = os.path.realpath(data_dir)

data_raw = "%s/raw" % data_dir
data_source = "%s/source" % data_dir
model_dir = "%s/models" % data_dir

ensure_dir_exists(data_dir)
ensure_dir_exists("%s/results" % data_dir)
ensure_dir_exists("%s/splitter" % data_dir)
ensure_dir_exists(data_raw)
ensure_dir_exists(data_source)
ensure_dir_exists(model_dir)

file_names = {
    'metrics': '%s/results/metrics.json' % data_dir,
    'train': '%s/splitter/train.csv' % data_dir,
    'validation': '%s/splitter/validation.csv' % data_dir,
    'raw_data': '%s/raw/store47-2016.csv' % data_dir,
    'full_model': '%s/full_model.pkl' % model_dir,
    'ml_params': 'ml_model_params.py',
    'encoder': '%s/encoder.json' % model_dir,
    'validation_plot': '%s/validation_plot.html' % model_dir,
    'raw_house_data': '%s/house_sales.csv' % data_raw,
    'house_data_zip_lookup': '%s/zip_lookup.csv' % data_raw,
    'pipeline_config': "%s/%s" % (config_dir, 'pipeline_config.yaml'),
    'dynamic_index': "%s/%s" % (template_dir, 'index_dynamic.html')
}
