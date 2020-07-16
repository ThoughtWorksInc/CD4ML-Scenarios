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

    def base_numerical_features(self, base_dict):
        base_num = self.params['base_numeric_fields']
        return {k: base_dict[k] for k in base_num}

    def base_categorical_features(self, base_dict):
        base_cat = list(self.params['base_categorical_n_levels_dict'].keys())
        return {k: base_dict[k] for k in base_cat}

    def ml_fields(self):
        categorical_n_levels_dict = self.params['base_categorical_n_levels_dict'].copy()

        categorical_n_levels_dict.update(self.params['derived_categorical_n_levels_dict'])
        numeric_fields = self.params['base_numeric_fields'] + \
            self.params['derived_numerical_fields']

        return {'categorical': categorical_n_levels_dict,
                'numerical': numeric_fields,
                'target_name': self.params['target_field']}

    def features(self, base_features_dict):
        base_num = self.base_numerical_features(base_features_dict)
        base_cat = self.base_categorical_features(base_features_dict)

        features = base_num
        features.update(base_cat)
        features.update(self.derived_features_numerical(base_features_dict))
        features.update(self.derived_features_categorical(base_features_dict))

        return features
