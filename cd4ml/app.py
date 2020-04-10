from flask import Flask, render_template, request
import cd4ml.app_utils as utils
from cd4ml.fluentd_logging import FluentdLogger

app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

fluentd_logger = FluentdLogger()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/replace_model', methods=["POST"])
def replace_model():
    content = request.get_data(as_text=False)
    utils.replace_model_file(content)
    return "OK", 200


@app.route('/replace_encoder', methods=["POST"])
def replace_encoder():
    content = request.get_data(as_text=False)
    utils.replace_encoder_file(content)
    return "OK", 200


@app.route('/prediction')
def get_prediction():
    date_string = request.args.get('date')
    item_nbr = request.args.get("item_nbr")

    prediction_tuple = utils.get_prediction(item_nbr, date_string)
    status = prediction_tuple[0]
    prediction = prediction_tuple[1]

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
        return "%d" % prediction, 200


def log_prediction_console(log_payload):
    print('logging {}'.format(log_payload))
