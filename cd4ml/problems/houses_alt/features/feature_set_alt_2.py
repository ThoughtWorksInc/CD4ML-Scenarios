from cd4ml.problems.houses_alt.features import feature_functions as ff
from cd4ml.feature_set import FeatureSetBase

feature_set_params = {'feature_set_name': 'feature_set_alt_2',
                      'target_field': 'price',
                      'extra_information_fields': [],
                      'base_categorical_n_levels_dict': {'zipcode': 50000,
                                                         'style': 50},
                      'base_fields_numerical': ['lot_size_sf', 'beds', 'baths', 'year_built',
                                                'kitchen_refurbished', 'square_feet', 'pool',
                                                'parking', 'multi_family'],
                      'derived_categorical_n_levels_dict': {'state': 100},
                      'derived_fields_numerical': [],
                      'encoder_excluded_fields': [],
                      'encoder_untransformed_fields': ['zipcode']}


class FeatureSet(FeatureSetBase):
    def __init__(self, zip_lookup):
        super(FeatureSet, self).__init__()
        self.params = feature_set_params.copy()

        # lookup table
        self.zip_lookup = zip_lookup

    # actually derive the fields

    def derived_features_categorical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']
        features = {'state': ff.zipcode_to_state(zipcode, self.zip_lookup)}
        return {k: features[k] for k in self.params['derived_categorical_n_levels_dict'].keys()}

    def derived_features_numerical(self, base_features):
        # some of these might not selected above
        zipcode = base_features['zipcode']

        features = {'avg_price_in_zip': ff.avg_price_by_zipcode(zipcode, self.zip_lookup),
                    'num_in_zip': ff.num_in_zipcode(zipcode, self.zip_lookup),
                    'avg_price_in_state': ff.avg_price_by_state(zipcode, self.zip_lookup),
                    'num_in_state': ff.num_in_state(zipcode, self.zip_lookup)}

        return {k: features[k] for k in self.params['derived_fields_numerical']}
