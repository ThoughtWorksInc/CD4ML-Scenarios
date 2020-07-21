from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso


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


def get_target_id_features_lists(pipeline_params, feature_set, processed_stream):
    identifier_name = pipeline_params['problem_params']['identifier']
    target_field = feature_set.params['target_field']
    features = []
    identifiers = []
    targets = []
    for row in processed_stream:
        features.append(feature_set.features(row))
        identifiers.append(row[identifier_name])
        targets.append(row[target_field])

    return targets, identifiers, features
