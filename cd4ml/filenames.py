"""
Keep all filename/path logic here rather than polluting code with hardcoded paths
"""
import os
from cd4ml.utils import ensure_dir_exists

data_dir_default = 'data'
data_dir = os.getenv('CD4ML_DATA_DIR', data_dir_default)
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
    'model': '%s/model.pkl' % model_dir,
    'ml_params': 'ml_model_params.py',
    'encoder': '%s/encoder.json' % model_dir,
    'validation_plot': '%s/validation_plot.html' % model_dir
}
