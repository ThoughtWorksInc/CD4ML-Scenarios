from cd4ml.problems.houses.features.feature_functions import zipcode_to_state
from cd4ml.feature_set import FeatureSet

feature_set_1_params = {'target_field': 'price',
                        'base_categorical_n_levels_dict': {'zipcode': 50000,
                                                           'style': 50,
                                                           'sale_id': 50},
                        'base_numeric_fields': ['lot_size_sf', 'beds', 'baths', 'year_built',
                                                'kitchen_refurbished', 'square_feet', 'pool',
                                                'parking', 'multi_family', 'price'],
                        'base_features_categorical_retain': ['style'],
                        'base_features_numerical_retain': ['lot_size_sf', 'beds',
                                                           'baths', 'year_built',
                                                           'kitchen_refurbished',
                                                           'square_feet', 'pool',
                                                           'parking', 'multi_family',
                                                           'price'],
                        'derived_categorical_n_levels_dict': {'state': 100},
                        'derived_numerical_fields': []}


class FeatureSet1(FeatureSet):
    def __init__(self, zip_lookup):
        super(FeatureSet1, self).__init__()
        self.zip_lookup = zip_lookup
        self.params = feature_set_1_params

    # actually derive the fields

    def derived_features_categorical(self, base_features):
        # assert False
        zipcode = base_features['zipcode']
        features = {'state': zipcode_to_state(zipcode, self.zip_lookup)}
        return {k: features[k] for k in self.params['derived_categorical_n_levels_dict'].keys()}

    def derived_features_numerical(self, base_features):
        features = {}
        return {k: features[k] for k in self.params['derived_numerical_fields']}
