problem_params = {'problem_name': 'houses',
                  'download_data_info': {
                       'url': "https://github.com/dave31415/house_price/raw/master/data/house_data_100000.csv",
                       'url_lookup': "https://github.com/dave31415/house_price/raw/master/data/zip_lookup.csv"
                   },
                  'model_name': 'random_forest',
                  'acceptance_metric': 'rms_score',
                  'acceptance_threshold_min': 0.0,
                  'acceptance_threshold_max': 125000,
                  'random_seed': 1299472653,
                  'training_seed': 4548276,
                  'identifier': 'sale_id',
                  'feature_set_name': 'feature_set_1',
                  'splitting': {
                    'training_random_start': 0.0,
                    'training_random_end': 0.1,
                    'validation_random_start': 0.7,
                    'validation_random_end': 1.0
                  },
                  'validation_metric_names': ['r2_score', 'rms_score', 'mad_score', 'num_validated']}
