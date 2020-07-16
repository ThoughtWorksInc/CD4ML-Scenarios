class RecordTransformer:
    def __init__(self, ml_fields, identifier_name, feature_set):
        self.ml_fields = ml_fields,
        self.target_name = ml_fields['target_name']
        self.identifier_name = identifier_name
        self.feature_set = feature_set

    def identifier(self, processed_row):
        return processed_row[self.identifier_name]

    def target(self, processed_row):
        if self.target_name in processed_row:
            return self.processed_row[self.target_name]
        else:
            return "TARGET_NOT_PRESENT"

    def base_features_numerical(self, processed_row):
        fields = [f for f in self.ml_fields['numerical']
                  if f not in [self.identifier_name, self.target_name]]

        return {f: processed_row[f] for f in fields}

    def base_features_categorical(self, processed_row):
        fields = [f for f in self.ml_fields['categorical']
                  if f not in [self.identifier_name, self.target_name]]

        return {f: processed_row[f] for f in fields}

    def base_features(self, processed_row):
        row = self.base_features_categorical(processed_row)
        row.update(self.base_features_numerical(processed_row))
        return row

    def base_features_categorical_retained(self, processed_row):
        return self.feature_set.base_features_categorical_retained(processed_row)

    def base_features_numerical_retained(self, processed_row):
        return self.feature_set.base_features_numerical_retained(processed_row)

    def base_features_retained(self, processed_row):
        row = self.base_features_categorical_retained(processed_row)
        row.update(self.base_features_numerical_retained(processed_row))
        return row

    def derived_features_categorical(self, processed_row):
        return self.feature_set.catgeorical_features(processed_row)

    def derived_features_numerical(self, processed_row):
        if self.feature_set is None:
            return {}

        return self.feature_set.numerical_features(processed_row)

    def derived_features(self, processed_row):
        row = self.derived_features_categorical(processed_row)
        row.update(self.derived_features_numerical(processed_row))
        return row

    def features(self, processed_row):
        row = self.base_features_retained(processed_row)
        row.update(self.derived_features(processed_row))
        return row
