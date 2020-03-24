import pandas as pd
import os
import json
import joblib
from sklearn import metrics
from cd4ml import evaluation
from cd4ml import tracking
from cd4ml.model_utils import get_model_class_and_params
from cd4ml.prepare_data import load_data, encode
from cd4ml.filenames import file_names


def train_model(train, model_name, seed=None):
    model_class, params = get_model_class_and_params(model_name)

    print("Training %s model" % model_name)
    train_dropped = train.drop('unit_sales', axis=1)
    target = train['unit_sales']

    clf = model_class(random_state=seed, **params)

    trained_model = clf.fit(train_dropped, target)
    return trained_model, params


def overwrite_unseen_prediction_with_zero(preds, train, validate):
    cols_item_store = ['item_nbr', 'store_nbr']
    cols_to_use = validate.columns.drop(
        'unit_sales') if 'unit_sales' in validate.columns else validate.columns
    validate_train_joined = pd.merge(
        validate[cols_to_use], train, on=cols_item_store, how='left')
    unseen = validate_train_joined[validate_train_joined['unit_sales'].isnull(
    )]
    validate['preds'] = preds
    validate.loc[validate.id.isin(unseen['id_x']), 'preds'] = 0
    preds = validate['preds'].tolist()
    return preds


def make_predictions(model, validate):
    print("Making prediction on validation data")
    validate_dropped = validate.drop('unit_sales', axis=1).fillna(-1)
    validate_preds = model.predict(validate_dropped)
    return validate_preds


def write_model(model):
    filename = file_names['model']
    print("Writing to {}".format(filename))
    joblib.dump(model, filename)


def write_predictions_and_score(evaluation_metrics):
    filename = 'results/metrics.json'
    print("Writing to {}".format(filename))
    if not os.path.exists('results'):
        os.makedirs('results')
    with open(filename, 'w+') as score_file:
        json.dump(evaluation_metrics, score_file)


def run_model(model_name='random_forest', seed=None):
    original_train, original_validate = load_data()
    train, validate = encode(original_train, original_validate)

    with tracking.track() as track:
        track.set_model(model_name)
        model, params = train_model(train, model_name, seed)
        track.log_params(params)
        validation_predictions = make_predictions(model, validate)

        print("Calculating metrics")
        evaluation_metrics = {
            'nwrmsle': evaluation.nwrmsle(validation_predictions,
                                          validate['unit_sales'].values,
                                          validate['perishable'].values),
            'r2_score': metrics.r2_score(y_true=validate['unit_sales'].values,
                                         y_pred=validation_predictions)
        }
        track.log_metrics(evaluation_metrics)

        write_predictions_and_score(evaluation_metrics)

        print("Evaluation done with metrics {}.".format(
            json.dumps(evaluation_metrics)))

        write_model(model)
