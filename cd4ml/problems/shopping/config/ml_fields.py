def get_ml_fields():
    categorical_n_levels_dict = {'item_nbr': 10000000000,
                                 'year': 50,
                                 'month': 13,
                                 'day': 370,
                                 'class': 600,
                                 'family': 100,
                                 'dayofweek': 10}

    numeric_fields = ['perishable',
                      'days_til_end_of_data',
                      'dayoff',
                      'unit_sales']

    target_field = 'unit_sales'

    ml_fields = {'categorical': categorical_n_levels_dict,
                 'numerical': numeric_fields,
                 'target_name': target_field}

    return ml_fields
