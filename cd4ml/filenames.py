"""
Keep all filename/path logic here rather than polluting code with hardcoded paths
"""
import os

data_dir_default = 'data'
data_dir = os.getenv('CD4ML_DATA_DIR', data_dir_default)

file_names = {
    'metrics': '%s/results/metrics.json' % data_dir,
    'train': '%s/splitter/train.csv' % data_dir,
    'validation': '%s/splitter/validation.csv' % data_dir
}
