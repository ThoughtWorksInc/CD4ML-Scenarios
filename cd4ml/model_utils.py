import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from cd4ml.filenames import get_filenames


def get_model_class(model_name):
    model_classes = {
        'random_forest': RandomForestRegressor,
        'adaboost': AdaBoostRegressor,
        'gradient_boosting': GradientBoostingRegressor,
        'decision_tree': DecisionTreeRegressor,
        'ridge': Ridge,
        'lasso': Lasso
    }

    return model_classes[model_name]


def get_target_id_features_lists(identifier_field, target_field, feature_set, processed_stream):
    features = []
    identifiers = []
    targets = []
    for row in processed_stream:
        features.append(feature_set.features(row))
        identifiers.append(row[identifier_field])
        targets.append(row[target_field])

    return targets, identifiers, features


def load_model(spec_name):
    problem_name = spec_name.split('#')[0]
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)
    loaded_model = joblib.load(file_names['full_model'])
    loaded_model.load_encoder_from_package()
    return loaded_model


def load_deployed_model(spec_name):
    problem_name = spec_name.split('#')[0]
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)
    loaded_model = joblib.load(file_names['full_model_deployed'])
    loaded_model.load_encoder_from_package()
    return loaded_model

def load_deployed_model_from_local_file(file_name):
    loaded_model = joblib.load(file_name)
    loaded_model.load_encoder_from_package()
    return loaded_model
