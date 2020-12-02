from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier

regressor_classes = {
        'random_forest': RandomForestRegressor,
        'adaboost': AdaBoostRegressor,
        'gradient_boosting': GradientBoostingRegressor,
        'decision_tree': DecisionTreeRegressor,
        'ridge': Ridge,
        'lasso': Lasso}

classifier_classes = {'random_forest_classifier': RandomForestClassifier}

algorithm_classes = regressor_classes.copy()
algorithm_classes.update(classifier_classes)


def get_model_type(model_name):
    regressor = model_name in regressor_classes
    classifier = model_name in classifier_classes

    if regressor and classifier:
        raise ValueError('model_name %s in BOTH regressors and classifiers, not allowed' % model_name)

    if not regressor and not classifier:
        raise ValueError('Model %s not recognized' % model_name)

    if regressor:
        return 'regressor'
    else:
        return 'classifier'


def get_algorithm_class(model_name):
    _ = get_model_type(model_name)
    return algorithm_classes[model_name]
