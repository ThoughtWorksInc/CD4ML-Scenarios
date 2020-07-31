"""
Web app
"""

from flask import Flask, request
from jinja2 import Template
from cd4ml.fluentd_logging import FluentdLogger
from cd4ml.dynamic_app import get_form_from_model
from cd4ml.filenames import get_filenames


app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

fluentd_logger = FluentdLogger()


def replace_model_file(content, problem_name):
    file_names = get_filenames(problem_name)
    with open(file_names['full_model_deployed'], 'w+b') as f:
        f.write(content)


@app.route('/replace_model/<problem_name>', methods=["post", "get"])
def replace_model(problem_name):
    print('Replacing model for problem: %s' % problem_name)
    content = request.get_data(as_text=False)
    data_length = len(content)
    print('data size: %s' % data_length)
    replace_model_file(content, problem_name)
    return "OK", 200


def log_prediction_console(log_payload):
    print('logging {}'.format(log_payload))


def dynamic_index_for_problem(problem_name):
    form_data = request.form
    if len(form_data) == 0:
        form_data = None

    header_text, form_div, prediction = get_form_from_model(problem_name, initial_values=form_data)
    if header_text == "ERROR":
        return "Error, model not loaded"

    file_names = get_filenames(problem_name)

    template_file = file_names['dynamic_index']
    template_text = open(template_file, 'r').read()
    template = Template(template_text)

    return template.render(header_text=header_text,
                           form_div=form_div,
                           prediction=prediction)


@app.route('/houses', methods=['get', 'post'])
def dynamic_index_houses():
    return dynamic_index_for_problem('houses')


@app.route('/groceries', methods=['get', 'post'])
def dynamic_index_groceries():
    return dynamic_index_for_problem('groceries')


@app.route('/', methods=['get', 'post'])
def not_a_route():
    messages = ["Must specify the problem",
                " Use /houses or /groceries routes"]

    return "\n".join(messages)
