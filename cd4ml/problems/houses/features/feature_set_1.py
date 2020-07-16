from cd4ml.problems.houses.features.feature_functions import avg_price_by_zipcode
from cd4ml.problems.houses.features.feature_functions import zipcode_to_state
from cd4ml.feature_set import FeatureSet


class FeatureSet1(FeatureSet):
    def __init__(self, zip_lookup):
        super(FeatureSet1, self).__init__()
        self.zip_lookup = zip_lookup

        # target variable
        self.target_field = 'price'

        # base field info
        self.base_categorical_n_levels_dict = {'zipcode': 50,
                                               'style': 50,
                                               'sale_id': 50}

        self.base_numeric_fields = ['lot_size_sf', 'beds', 'baths', 'year_built',
                                    'kitchen_refurbished', 'square_feet', 'pool',
                                    'parking', 'multi_family', 'price']

        # derived field info

        self.derived_categorical_n_levels_dict = {'state': 100}
        # self.derived_numerical_fields = ['avg_price_for_zip']
        self.derived_numerical_fields = []

        self.base_features_categorical_retain = ['style']
        self.base_features_numerical_retain = ['lot_size_sf', 'beds',
                                               'baths', 'year_built',
                                               'kitchen_refurbished',
                                               'square_feet', 'pool',
                                               'parking', 'multi_family',
                                               'price']

    def base_features_categorical_retained(self, base_features):
        return {k: base_features[k] for k in self.base_features_categorical_retain}

    def base_features_numerical_retained(self, base_features):
        return {k: base_features[k] for k in self.base_features_numerical_retain}

    def derived_features_categorical(self, base_features):
        # assert False
        zipcode = base_features['zipcode']
        features = {'state': zipcode_to_state(zipcode, self.zip_lookup)}
        return {k: features[k] for k in self.derived_categorical_n_levels_dict.keys()}

    def derived_features_numerical(self, base_features):
        # zipcode = base_features['zipcode']
        # features = {'avg_price_for_zip': avg_price_by_zipcode(zipcode, self.zip_lookup)}
        features = {}
        return {k: features[k] for k in self.derived_numerical_fields}
