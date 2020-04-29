# parameters specific to the problem and it's data

problem_params = {'problem_name': 'shopping',
                  'max_date': '2017-08-15',
                  'days_back': 57,
                  'data_source': 'file',
                  'download_data_info': {
                       'key': 'store47-2016.csv',
                       'gcs_bucket': 'continuous-intelligence',
                       'base_url': 'https://storage.googleapis.com'
                   },
                  'model_name': 'random_forest',
                  'acceptance_metric': 'r2_score',
                  'acceptance_threshold_min': 0.60,
                  'acceptance_threshold_max': 1.0,
                  'random_seed': 452833122,
                  'validation_metric_names': ['r2_score', 'rms_score', 'mad_score', 'num_validated']}
