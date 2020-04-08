# parameters for running the pipeline
from cd4ml.ml_model_params import model_parameters

pipeline_params = {'model_name': 'random_forest',
                   'data_reader': {
                       'type': 'file'
                   },
                   'model_params': model_parameters,
                   'download_data_info':
                       {
                           'key': 'store47-2016.csv',
                           'gcs_bucket': 'continuous-intelligence',
                           'base_url': 'https://storage.googleapis.com/%s/%s'
                       }}
