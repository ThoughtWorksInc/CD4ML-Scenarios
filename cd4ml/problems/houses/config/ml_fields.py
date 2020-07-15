def get_ml_fields():
    categorical_n_levels_dict = {'zipcode': 50000,
                                 'style': 50,
                                 'sale_id': 50}

    numeric_fields = ['lot_size_sf', 'beds', 'baths', 'year_built', 'kitchen_refurbished',
                      'square_feet', 'pool', 'parking', 'multi_family', 'price']

    target_field = 'price'

    ml_fields = {'categorical': categorical_n_levels_dict,
                 'numerical': numeric_fields,
                 'target_name': target_field}

    return ml_fields
