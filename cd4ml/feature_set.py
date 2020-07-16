class FeatureSet:
    """
    Generic interface for feature sets
    """
    def __init__(self):
        # fields to be filled out in derived class
        self.params = None

    def derived_features_categorical(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def derived_features_numerical(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def base_features_categorical_retained(self, base_features):
        return {k: base_features[k] for k in self.params['base_features_categorical_retain']}

    def base_features_numerical_retained(self, base_features):
        return {k: base_features[k] for k in self.params['base_features_numerical_retain']}

    def ml_fields(self):
        categorical_n_levels_dict = {k: v for k, v in self.params['base_categorical_n_levels_dict'].items()
                                     if k in self.params['base_features_categorical_retain']}

        categorical_n_levels_dict.update(self.params['derived_categorical_n_levels_dict'])
        numeric_fields = self.params['base_features_numerical_retain'] + \
            self.params['derived_numerical_fields']

        return {'categorical': categorical_n_levels_dict,
                'numerical': numeric_fields,
                'target_name': self.params['target_field']}

    def features(self, base_features):
        features = self.base_features_numerical_retained(base_features)
        features.update(self.derived_features_numerical(base_features))
        features.update(self.base_features_categorical_retained(base_features))
        features.update(self.derived_features_categorical(base_features))
        return features
