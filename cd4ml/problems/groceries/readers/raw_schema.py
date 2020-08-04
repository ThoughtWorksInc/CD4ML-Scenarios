base_categorical = ['id', 'date', 'item_nbr', 'family', 'class', 'dayoff']

base_numeric = ['unit_sales', 'perishable', 'transactions', 'days_til_end_of_data',
                'year', 'month', 'day', 'dayofweek']

raw_schema = {'categorical': base_categorical,
              'numerical': base_numeric}
