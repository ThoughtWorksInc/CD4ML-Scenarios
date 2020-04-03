model_params = {
    "random_forest": {
        "n_estimators": 50
    },
    "adaboost": {
        "n_estimators": 50,
        "learning_rate": 1.0,
        "loss": "linear"
    },
    "adaboost_regressor": {
        "n_estimators": 200,
        "max_depth": 4
    },
    "gradient_boosting": {
        "n_estimators": 200,
        "max_depth": 4
    },
    "decision_tree": {
        'criterion': 'mse'
    },
    "data_reader": {
        "type": "postgres",
        "host": "psql",
        "username": "postgres",
        "password": "<A_S3cur3_Password>",
        "database": "cd4ml"
    }
}
