from flask import Flask, render_template, request
from jinja2 import Template
import cd4ml.app_utils as utils
from cd4ml.fluentd_logging import FluentdLogger
from cd4ml.dynamic_app import get_form_from_model
from cd4ml.filenames import file_names

app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

fluentd_logger = FluentdLogger()


@app.route('/old')
def index():
    return render_template('index.html')


@app.route('/replace_model', methods=["POST"])
def replace_model():
    content = request.get_data(as_text=False)
    utils.replace_model_file(content)
    return "OK", 200


@app.route('/prediction')
def get_prediction():
    date_string = request.args.get('date')
    item_nbr = request.args.get("item_nbr")

    status, prediction = utils.get_prediction(item_nbr, date_string)

    log_payload = {
        'prediction': prediction,
        'itemid': item_nbr,
        'item_name': utils.get_product_name_from_id(item_nbr),
        'date_string': date_string
    }

    log_prediction_console(log_payload)
    fluentd_logger.log('prediction', log_payload)

    if status == "ERROR":
        return prediction, 503
    else:
        return "%0.5f" % prediction, 200


def log_prediction_console(log_payload):
    print('logging {}'.format(log_payload))


@app.route('/', methods=['get', 'post'])
def dynamic_index():
    form_data = request.form
    print('form_data')
    print(form_data)
    if len(form_data) == 0:
        form_data = None

    header_text, form_div, prediction = get_form_from_model(initial_values=form_data)

    template_file = file_names['dynamic_index']
    template_text = open(template_file, 'r').read()
    template = Template(template_text)

    return template.render(header_text=header_text,
                           form_div=form_div,
                           prediction=prediction)
