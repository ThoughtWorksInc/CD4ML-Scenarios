class FeatureSet:
    """
    Generic interface for feature sets
    """
    def __init__(self):
        # fields to be filled out in derived class
        self.base_categorical_n_levels_dict = None
        self.base_features_categorical_retain = None
        self.derived_categorical_n_levels_dict = None
        self.base_features_numerical_retain = None
        self.derived_numerical_fields = None
        self.target_field = None

    def base_features_categorical_retained(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def base_features_numerical_retained(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def derived_features_categorical(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def derived_features_numerical(self, base_features):
        assert isinstance(base_features, dict)
        return {}

    def ml_fields(self):
        categorical_n_levels_dict = {k: v for k, v in self.base_categorical_n_levels_dict.items()
                                     if k in self.base_features_categorical_retain}

        categorical_n_levels_dict.update(self.derived_categorical_n_levels_dict)
        numeric_fields = self.base_features_numerical_retain + self.derived_numerical_fields

        return {'categorical': categorical_n_levels_dict,
                'numerical': numeric_fields,
                'target_name': self.target_field}

    def features(self, base_features):
        features = self.base_features_numerical_retained(base_features)
        features.update(self.derived_features_numerical(base_features))
        features.update(self.base_features_categorical_retained(base_features))
        features.update(self.derived_features_categorical(base_features))
        return features
