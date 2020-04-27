# parameters specific to the problem and it's data

problem_params = {'problem': 'shopping',
                  'days_back': 57,
                  'data_source': 'file',
                  'download_data_info': {
                       'key': 'store47-2016.csv',
                       'gcs_bucket': 'continuous-intelligence',
                       'base_url': 'https://storage.googleapis.com'
                   },
                  'target_name': 'unit_sales',
                  'model_name': 'random_forest',
                  'acceptance_metric': 'r2_score',
                  'acceptance_threshold_min': 0.60,
                  'acceptance_threshold_max': 1.0}
