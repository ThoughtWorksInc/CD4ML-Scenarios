problem_params = {'problem_name': 'houses',
                  'download_data_info': {
                       'url': "https://github.com/dave31415/house_price/raw/master/data/house_data_100000.csv"
                   },
                  'model_name': 'random_forest',
                  'acceptance_metric': 'r2_score',
                  'acceptance_threshold_min': 0.0,
                  'acceptance_threshold_max': 1.0,
                  'random_seed': 1299472653,
                  'identifier': 'sale_id',
                  'splitting': {
                    'training_random_start': 0.0,
                    'training_random_end': 0.2,
                    'validation_random_start': 0.8,
                    'validation_random_end': 1.0
                  },
                  'validation_metric_names': ['r2_score', 'rms_score', 'mad_score', 'num_validated']}
