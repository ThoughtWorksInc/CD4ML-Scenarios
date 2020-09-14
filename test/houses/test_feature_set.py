from cd4ml.problems.houses.features.feature_sets.default.feature_set \
    import FeatureSet as FeatureSetDefault, get_feature_set_params as get_feature_set_params_default
from cd4ml.problems.houses.features.feature_sets.simple.feature_set \
    import FeatureSet as FeatureSetSimple, get_feature_set_params as get_feature_set_params_simple


feature_set_params_default_provided = {
    'feature_set_name': 'default',
    'extra_information_fields': [],
    'base_categorical_n_levels_dict': {'zipcode': 50000,
                                       'style': 50},
    'base_fields_numerical': ['lot_size_sf', 'beds', 'baths', 'year_built',
                              'kitchen_refurbished', 'square_feet', 'pool',
                              'parking', 'multi_family'],
    'derived_categorical_n_levels_dict': {'state': 100},
    'derived_fields_numerical': ['avg_price_in_zip', 'num_in_zip',
                                 'avg_price_in_state', 'num_in_state',
                                 ],
    'encoder_excluded_fields': [],
    'encoder_untransformed_fields': ['zipcode']}


feature_set_params_simple_provided = {
    "feature_set_name": "feature_set_simple",
    "extra_information_fields": [],
    "base_categorical_n_levels_dict": {
        "zipcode": 50000,
        "style": 50
    },
    "base_fields_numerical": [
        "lot_size_sf",
        "beds",
        "baths",
        "square_feet"
    ],
    "derived_categorical_n_levels_dict": {
        "state": 100
    },
    "derived_fields_numerical": [
        "avg_price_in_zip"
    ],
    "encoder_excluded_fields": [],
    "encoder_untransformed_fields": [
        "zipcode"
    ]
}


def check_feature_set(use_json_file, feature_set_class):

    if feature_set_class == FeatureSetDefault:
        derived_info = {
            "state": "MA",
            "avg_price_in_zip": 700000,
            "num_in_zip": 100,
            "avg_price_in_state": 500000,
            "num_in_state": 90000
        }

        feature_set_params_provided = feature_set_params_default_provided
        delete_fields = []

    elif feature_set_class == FeatureSetSimple:
        derived_info = {
            "state": "MA",
            "avg_price_in_zip": 700000
        }

        feature_set_params_provided = feature_set_params_simple_provided
        delete_fields = ['year_built', 'kitchen_refurbished', 'pool', 'parking', 'multi_family']

    else:
        raise ValueError('Unknown class')

    identifier_field = 'sale_id'
    target_field = 'price'
    zip_lookup = {
        "02186": {
            "state": "MA",
            "avg_price_in_zip": 700000,
            "num_in_zip": 100,
            "avg_price_in_state": 500000,
            "num_in_state": 90000
        }
    }

    info = {'zip_lookup': zip_lookup}

    if use_json_file:
        if feature_set_class == FeatureSetDefault:
            feature_set_params = get_feature_set_params_default()
        elif feature_set_class == FeatureSetSimple:
            feature_set_params = get_feature_set_params_simple()
        else:
            raise ValueError('Unknown class')

    else:
        feature_set_params = feature_set_params_provided

    feature_set = feature_set_class(identifier_field, target_field, info, feature_set_params)

    assert feature_set.info == info

    processed_row = {'zipcode': '02186',
                     'style': 'victorian',
                     'sale_id': 'foo',
                     'lot_size_sf': 8200,
                     'beds': 4,
                     'baths': 2,
                     'year_built': 1886,
                     'kitchen_refurbished': 1,
                     'square_feet': 2200,
                     'pool': 1,
                     'parking': 1,
                     'multi_family': 0,
                     'price': 820000}

    assert feature_set.info == info

    features = feature_set.features(processed_row)

    expected = processed_row.copy()

    expected.update(derived_info)

    del expected['price']
    del expected['sale_id']

    for field in delete_fields:
        del expected[field]

    expected.update(derived_info)

    assert features == expected


def test_feature_set_default_with_json():
    # will fail if json file changes
    check_feature_set(True, FeatureSetDefault)


def test_feature_set_default_with_explicit_params():
    # test should pass even if json file changes
    # because explicit params are passed in
    check_feature_set(False, FeatureSetDefault)


def test_feature_set_simple_with_json():
    # will fail if json file changes
    check_feature_set(True, FeatureSetSimple)


def test_feature_set_simple_with_explicit_params():
    # test should pass even if json file changes
    # because explicit params are passed in
    check_feature_set(False, FeatureSetSimple)
