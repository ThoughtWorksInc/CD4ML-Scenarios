model_parameters = {
    "random_forest": {
        "n_estimators": 70,
        "max_features": 0.4
    },
    "adaboost": {
        "n_estimators": 100
    },
    "gradient_boosting": {
        "n_estimators": 70,
        "max_depth": 6
    },
    "decision_tree": {
        "criterion": 'mse'
    },
    "ridge": {
        "normalize": "true",
        "alpha": 1.0
    },
    "lasso": {
        "normalize": "true",
        "alpha": 1.0
    }
}
