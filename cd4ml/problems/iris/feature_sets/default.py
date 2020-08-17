from cd4ml.feature_set import FeatureSetBase

feature_set_params = {'feature_set_name': 'default',
                      'extra_information_fields': [],
                      'base_categorical_n_levels_dict': {'species': 50000},
                      'base_fields_numerical': ['sepal_length', 'sepal_width',
                                                'petal_length', 'petal_width'],
                      'derived_categorical_n_levels_dict': {},
                      'derived_fields_numerical': [],
                      'encoder_excluded_fields': [],
                      'encoder_untransformed_fields': []}


class FeatureSet(FeatureSetBase):
    def __init__(self, identifier_field, target_field, info):
        super(FeatureSet, self).__init__(identifier_field, target_field)
        self.info = info
        self.params = feature_set_params.copy()

    # actually derive the fields

    def derived_features_categorical(self, base_features):
        return {}

    def derived_features_numerical(self, base_features):
        return {}
