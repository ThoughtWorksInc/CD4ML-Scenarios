problem_params = {'problem_name': 'groceries',
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
                  'acceptance_threshold_min': 0.6,
                  'acceptance_threshold_max': 1.0,
                  'random_seed': 452833122,
                  'training_seed': 2245486,
                  'identifier_field': 'id',
                  'feature_set_name': 'feature_set_1',
                  'max_rows_to_read': None,
                  'splitting': {
                    'training_random_start': 0.0,
                    'training_random_end': 0.7,
                    'validation_random_start': 0.7,
                    'validation_random_end': 1.0
                  },
                  'validation_metric_names': ['r2_score', 'rms_score', 'mad_score', 'num_validated']}
