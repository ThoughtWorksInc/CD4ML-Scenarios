"""
Web app
"""

from flask import Flask, request
from jinja2 import Template
from cd4ml.fluentd_logging import FluentdLogger
from cd4ml.dynamic_app import get_form_from_model, list_available_models
from cd4ml.filenames import get_filenames


app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

fluentd_logger = FluentdLogger()


def replace_model_file(content, spec_name):
    problem_name = spec_name.split('$')[0]
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)
    with open(file_names['full_model_deployed'], 'w+b') as f:
        f.write(content)


@app.route('/replace_model/<spec_name>', methods=["post"])
def replace_model(spec_name):
    print('Replacing model for problem spec: %s' % spec_name)
    content = request.get_data(as_text=False)
    data_length = len(content)
    print('data size: %s' % data_length)
    replace_model_file(content, spec_name)
    return "OK", 200


def log_prediction_console(log_payload):
    print('logging {}'.format(log_payload))


def dynamic_index_for_problem(spec_name):
    form_data = request.form
    if len(form_data) == 0:
        form_data = None

    header_text, form_div, prediction = get_form_from_model(spec_name, initial_values=form_data)
    if header_text == "ERROR":
        return "Error, model not loaded"

    problem_name = spec_name.split('$')[0]
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)

    template_file = file_names['dynamic_index']
    template_text = open(template_file, 'r').read()
    template = Template(template_text)

    return template.render(header_text=header_text,
                           form_div=form_div,
                           prediction=prediction)


@app.route('/<spec_name>', methods=['get', 'post'])
def dynamic_index_houses(spec_name):
    return dynamic_index_for_problem(spec_name)


def spec_to_dict(spec, num):
    fields = ['problem_name', 'ml_pipeline_params_name', 'feature_set_name',
              'algorithm_name', 'algorithm_params_name']

    values = spec.split('$')
    data = {f: v for f, v in zip(fields, values)}
    data['num'] = num
    data['spec'] = spec
    data['url'] = '/'+spec
    return data


@app.route('/', methods=['get', 'post'])
def not_a_route():
    available_models = sorted(list_available_models())
    model_data = [spec_to_dict(spec, num) for num, spec in enumerate(available_models)]

    file_names = get_filenames('')
    template_file = file_names['index_models']
    template_text = open(template_file, 'r').read()
    template = Template(template_text)

    print(model_data)
    return template.render(rows=model_data)
