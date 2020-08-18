import joblib


def get_target_id_features_lists(identifier_field, target_field, feature_set, processed_stream):
    features = []
    identifiers = []
    targets = []
    for row in processed_stream:
        features.append(feature_set.features(row))
        identifiers.append(row[identifier_field])
        targets.append(row[target_field])

    return targets, identifiers, features


def load_deployed_model_from_local_file(file_name):
    loaded_model = joblib.load(file_name)
    loaded_model.load_encoder_from_package()
    return loaded_model
