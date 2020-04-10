# parameters for running the pipeline
from cd4ml.ml_model_params import model_parameters

# TODO: add some security protocols around the key?

pipeline_params = {'model_name': 'random_forest',
                   'days_back': 57,
                   'acceptance_metric': 'r2_score',
                   'acceptance_threshold_min': 0.60,
                   'acceptance_threshold_max': 1.0,
                   'data_source': 'file',
                   'model_params': model_parameters,
                   'download_data_info': {
                       'key': 'store47-2016.csv',
                       'gcs_bucket': 'continuous-intelligence',
                       'base_url': 'https://storage.googleapis.com'
                   }}
