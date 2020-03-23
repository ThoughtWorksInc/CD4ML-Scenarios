import pandas as pd
import os
import json
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn import metrics
from cd4ml import evaluation
from cd4ml import tracking
from cd4ml.filenames import file_names
from cd4ml.model_utils import get_model_class_and_params


def load_data():
    filename = file_names['train']
    print("Loading data from {}".format(filename))
    train = pd.read_csv(filename)

    filename = file_names['validation']
    print("Loading data from {}".format(filename))
    validate = pd.read_csv(filename)

    return train, validate


def join_tables(train, validate):
    print("Joining tables for consistent encoding")
    return train.append(validate).drop('date', axis=1)


def encode_categorical_columns(df):
    obj_df = df.select_dtypes(include=['object', 'bool']).copy().fillna('-1')
    lb = LabelEncoder()
    for col in obj_df.columns:
        df[col] = lb.fit_transform(obj_df[col])
    return df


def encode(train, validate):
    print("Encoding categorical variables")
    train_ids = train.id
    validate_ids = validate.id

    joined = join_tables(train, validate)

    encoded = encode_categorical_columns(joined.fillna(-1))

    print("Not predicting returns...")
    encoded.loc[encoded.unit_sales < 0, 'unit_sales'] = 0

    validate = encoded[encoded['id'].isin(validate_ids)]
    train = encoded[encoded['id'].isin(train_ids)]
    return train, validate


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


def write_predictions_and_score(evaluation_metrics, model, columns_used):
    key = "decision_tree"
    if not os.path.exists('data/{}'.format(key)):
        os.makedirs('data/{}'.format(key))
    filename = 'data/{}/model.pkl'.format(key)
    print("Writing to {}".format(filename))
    joblib.dump(model, filename)

    filename = 'results/metrics.json'
    print("Writing to {}".format(filename))
    if not os.path.exists('results'):
        os.makedirs('results')
    with open(filename, 'w+') as score_file:
        json.dump(evaluation_metrics, score_file)


def main(model_name='random_forest', seed=None):
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

        write_predictions_and_score(
            evaluation_metrics, model, original_train.columns)

        print("Evaluation done with metrics {}.".format(
            json.dumps(evaluation_metrics)))
