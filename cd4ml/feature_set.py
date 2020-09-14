import logging


def _exclude(fields, excluded):
    return [field for field in fields if field not in excluded]


def _combine_dicts(*args):
    results = {}
    for arg in args:
        results.update(arg)

    return results


class FeatureSetBase:
    """
    Generic interface for feature sets
    """
    def __init__(self, identifier_field, target_field):
        # fields to be filled out in derived class
        self.logger = logging.getLogger(__name__)
        self.params = None
        self.info = None
        self.identifier_field = identifier_field
        self.target_field = target_field

    def fields_excluded_from_features(self):
        id_target = [self.identifier_field, self.target_field]
        return id_target + self.params['extra_information_fields']

    def _exclude_non_features(self, fields):
        return _exclude(fields, self.fields_excluded_from_features())

    def base_feature_fields_numerical(self):
        fields = self.params['base_fields_numerical']
        return self._exclude_non_features(fields)

    def base_feature_fields_categorical(self):
        fields = sorted(self.params['base_categorical_n_levels_dict'].keys())
        return self._exclude_non_features(fields)

    def base_feature_fields(self):
        return self.base_feature_fields_numerical() + self.base_feature_fields_categorical()

    def derived_feature_fields_numerical(self):
        return self.params['derived_fields_numerical']

    def derived_feature_fields_categorical(self):
        return sorted(self.params['derived_categorical_n_levels_dict'].keys())

    def derived_feature_fields(self):
        return self.derived_feature_fields_numerical() + self.derived_feature_fields_categorical()

    def available_feature_fields_numerical(self):
        return self.base_feature_fields_numerical() + self.derived_feature_fields_numerical()

    def available_feature_fields_categorical(self):
        return self.base_feature_fields_categorical() + self.derived_feature_fields_categorical()

    def encoded_feature_fields_numerical(self):
        return _exclude(self.available_feature_fields_numerical(), self.params['encoder_excluded_fields'])

    def encoded_feature_fields_categorical(self):
        return _exclude(self.available_feature_fields_categorical(), self.params['encoder_excluded_fields'])

    def encoded_feature_fields(self):
        return self.encoded_feature_fields_numerical() + self.encoded_feature_fields_categorical()

    def omitted_feature_fields_for_input(self):
        encoded = self.encoded_feature_fields()
        return [field for field in encoded if field not in self.base_feature_fields()]

    # feature transformations

    def base_features_numerical(self, processed_row):
        return {k: processed_row[k] for k in self.base_feature_fields_numerical()}

    def base_features_categorical(self, processed_row):
        return {k: processed_row[k] for k in self.base_feature_fields_categorical()}

    def base_features(self, processed_row):
        return {k: processed_row[k] for k in self.base_feature_fields()}

    def derived_features_categorical(self, processed_row):
        # TODO: override
        assert isinstance(processed_row, dict)
        return {}

    def derived_features_numerical(self, processed_row):
        # TODO: override
        assert isinstance(processed_row, dict)
        return {}

    def derived_features(self, processed_row):
        num = self.derived_features_numerical(processed_row)
        cat = self.derived_features_categorical(processed_row)
        return _combine_dicts(num, cat)

    def features(self, processed_row):
        base = self.base_features(processed_row)
        derv = self.derived_features(processed_row)
        return _combine_dicts(base, derv)

    def ml_fields(self):
        categorical_n_levels_dict = self.params['base_categorical_n_levels_dict'].copy()
        categorical_n_levels_dict.update(self.params['derived_categorical_n_levels_dict'])

        cat_encoded = {k: v for k, v in categorical_n_levels_dict.items()
                       if k in self.encoded_feature_fields_categorical()}

        numeric_fields = self.encoded_feature_fields_numerical()

        intersection = set(cat_encoded.keys()).intersection(numeric_fields)

        if intersection:
            self.logger.info('categorical')
            self.logger.info(cat_encoded)
            self.logger.info('numerical')
            self.logger.info(numeric_fields)
            self.logger.info('intersection')
            self.logger.info(intersection)
            raise ValueError('categorical and numeric overlap')

        return {'categorical': cat_encoded,
                'numerical': numeric_fields,
                'target_name': self.target_field}
