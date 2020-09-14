"""
Web app
"""
import logging

import requests
from flask import Flask, request, render_template

from cd4ml.logger.fluentd_logging import FluentdLogger
from cd4ml.webapp.model_cache import ModelCache
from cd4ml.webapp.webapp_data_scorer import get_form_from_model

logger = logging.getLogger(__name__)
fluentd_logger = FluentdLogger()
cache = ModelCache()

ERROR_NO_AVAILABLE_LATEST_MODEL = "No model is available for the latest scenario {}. " \
                                  "Please re-run jenkins and reload this page"
ERROR_NO_MODEL_AT_LOCATION = "No model is available for this identifier scenario {}. " \
                             "Please navigate back to the model picker and try again."

app = Flask(__name__,
            template_folder='webapp/templates',
            static_folder='webapp/static')


def make_page_for_scenario_and_identifier(scenario_name, identifier, request_data):
    model = cache.get_loaded_model_for_scenario_and_run_id(scenario_name, identifier)
    header_text, form_div, prediction = get_form_from_model(scenario_name, identifier, model,
                                                            initial_values=request_data)
    return header_text, form_div, prediction


def return_all_models_for_scenario(scenario):
    try:
        all_models = cache.list_available_models_from_ml_flow()
        return render_template("model_list.html",
                               printable_scenario_name=scenario,
                               scenario_name=scenario,
                               rows=all_models.get(scenario))
    except requests.exceptions.ConnectionError as e:
        logger.error("Could not connect to MLFlow", exc_info=e)
        return render_template("error.html",
                               title="Could not connect to MLFlow",
                               message="Error connecting to MLFlow to retrieve all models. P"
                                       "lease ensure that MLFlow is running.")


def check_that_page_can_be_loaded(scenario_name, identifier):
    try:
        return cache.get_loaded_model_for_scenario_and_run_id(scenario_name, identifier) is not None
    except requests.exceptions.ConnectionError as e:
        logger.error("Could not access mlflow", exc_info=e)
        return False


@app.route('/', methods=['get'])
@app.route('/index.html', methods=['get'])
def welcome():
    return render_template("index.html")


@app.route('/api/<scenario_name>/<identifier>', methods=['post'])
def call_model_for_scenario_and_identifier(scenario_name, identifier=None):
    json_body = request.json
    if len(json_body) == 0:
        return {
            "error": "No content supplied"
        }

    _, _, prediction = make_page_for_scenario_and_identifier(scenario_name, identifier, json_body)
    if prediction is not None:
        logging_object = dict(json_body)
        logging_object['prediction'] = prediction
        logging_object['scenario'] = scenario_name
        logging_object['identifier'] = identifier
        fluentd_logger.log("prediction", logging_object)

    return prediction if prediction is not None else {
        "error": "No Model Available To Use"
    }


@app.route('/<scenario_name>/<identifier>', methods=['get', 'post'])
def return_webpage_for_scenario_and_identifier(scenario_name, identifier):
    # If this is models, return the model list table
    if identifier == "models":
        return return_all_models_for_scenario(scenario_name)

    # Verify that there is a model to use,
    form_data = request.form
    if len(form_data) == 0:
        has_backing_model = check_that_page_can_be_loaded(scenario_name, identifier)
        if has_backing_model is False:
            message = (ERROR_NO_AVAILABLE_LATEST_MODEL if identifier == "latest" else ERROR_NO_MODEL_AT_LOCATION)\
                .format(scenario_name)
            return render_template("error.html",
                                   title="No model available to use",
                                   message=message)
        form_data = None

    # There is a model, run and return the output
    identifier_to_use = "latest" if identifier is None else identifier
    _, form_div, prediction = make_page_for_scenario_and_identifier(scenario_name, identifier_to_use, form_data)

    if prediction is not None:
        logging_object = dict(form_data)
        logging_object['prediction'] = prediction
        logging_object['scenario'] = scenario_name
        logging_object['identifier'] = identifier
        fluentd_logger.log("prediction", logging_object)

    return render_template("results.html",
                           title=f"Predicting for Scenario {scenario_name}",
                           form_div=form_div,
                           prediction=prediction)
