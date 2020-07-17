from cd4ml.problems.houses.features.feature_functions import zipcode_to_state, num_in_zipcode
from cd4ml.problems.houses.features.feature_functions import avg_price_by_zipcode
from cd4ml.feature_set import FeatureSet

feature_set_1_params = {'feature_set_name': 'feature_set_1',
                        'target_field': 'price',
                        'base_categorical_n_levels_dict': {'zipcode': 50000,
                                                           'style': 50},
                        'base_numeric_fields': ['lot_size_sf', 'beds', 'baths', 'year_built',
                                                'kitchen_refurbished', 'square_feet', 'pool',
                                                'parking', 'multi_family', 'price'],
                        'base_features_omitted': ['zipcode'],
                        'derived_categorical_n_levels_dict': {'state': 100},
                        'derived_numerical_fields': ['avg_price_in_zip', 'num_in_zip']}


class FeatureSet1(FeatureSet):
    def __init__(self, zip_lookup):
        super(FeatureSet1, self).__init__()
        self.zip_lookup = zip_lookup
        self.params = feature_set_1_params.copy()

    # actually derive the fields

    def derived_features_categorical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']
        features = {'state': zipcode_to_state(zipcode, self.zip_lookup)}
        return {k: features[k] for k in self.params['derived_categorical_n_levels_dict'].keys()}

    def derived_features_numerical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']

        features = {'avg_price_in_zip': avg_price_by_zipcode(zipcode, self.zip_lookup),
                    'num_in_zip': num_in_zipcode(zipcode, self.zip_lookup)}

        return {k: features[k] for k in self.params['derived_numerical_fields']}
