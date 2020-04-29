problem_params = {'problem_name': 'zillow',
                  'download_data_info': {
                       'url': "https://github.com/dave31415/zillow_data_small/archive/master.zip"
                   },
                  'model_name': 'random_forest',
                  'acceptance_metric': 'r2_score',
                  'zillow_year': 2016,
                  'acceptance_threshold_min': 0.0,
                  'acceptance_threshold_max': 1.0,
                  'random_seed': 1299472653,
                  'identifier': 'parcelid',
                  'splitting': {
                    'training_random_start': 0.0,
                    'training_random_end': 0.3,
                    'validation_random_start': 0.7,
                    'validation_random_end': 1.0
                  },
                  'validation_metric_names': ['r2_score', 'rms_score', 'mad_score', 'num_validated']}
