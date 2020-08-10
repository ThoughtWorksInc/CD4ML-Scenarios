"""
Web app
"""

from flask import Flask, request, render_template
from cd4ml.webapp.webapp_data_scorer import get_form_from_model

import logging

from cd4ml.logger.fluentd_logging import FluentdLogger
from cd4ml.webapp.model_cache import ModelCache

logger = logging.getLogger(__name__)
fluentd_logger = FluentdLogger()
cache = ModelCache()

app = Flask(__name__,
            template_folder='webapp/templates',
            static_folder='webapp/static')


def dynamic_index_for_problem(scenario_name, identifier):
    form_data = request.form
    if len(form_data) == 0:
        form_data = None

    model = cache.get_loaded_model_for_scenario_and_run_id(scenario_name, identifier)
    header_text, form_div, prediction = get_form_from_model(scenario_name, model, initial_values=form_data)
    if header_text == "ERROR":
        return "Error, model not loaded"

    return render_template("index_dynamic.html",
                           header_text=header_text,
                           form_div=form_div,
                           prediction=prediction)


def return_all_models_for_scenario(scenario):
    all_models = cache.list_available_models_from_ml_flow()
    return render_template("index_models.html",
                           printable_scenario_name=scenario,
                           scenario_name=scenario,
                           rows=all_models[scenario])


@app.route('/', methods=['get'])
@app.route('/index.html', methods=['get'])
def welcome():
    return render_template("index.html")


@app.route('/<scenario_name>/<identifier>', methods=['get'])
def dynamic_index_houses(scenario_name, identifier=None):
    if identifier == "models":
        return return_all_models_for_scenario(scenario_name)
    elif identifier == "latest":
        return dynamic_index_for_problem(scenario_name, "latest")
    else:
        return dynamic_index_for_problem(scenario_name, identifier)
