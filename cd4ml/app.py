from flask import Flask, render_template, request
import os
from fluent import sender
import cd4ml.app_utils as utils

app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

TENANT = os.getenv('TENANT', 'model')
FLUENTD_HOST = os.getenv('FLUENTD_HOST')
FLUENTD_PORT = os.getenv('FLUENTD_PORT')

print("FLUENTD_HOST="+FLUENTD_HOST)
print("FLUENTD_PORT="+FLUENTD_PORT)


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
    predicition = prediction_tuple[1]

    log_payload = {'prediction': predicition, 
                   'itemid': item_nbr, 
                   'item_name': utils.get_product_name_from_id(item_nbr), 
                   'date_string': date_string}
    log_prediction_console(log_payload)

    if FLUENTD_HOST is not None:
        log_prediction_fluentd(log_payload)

    if status == "ERROR":
        return predicition, 503
    else:
        return "%d" % predicition, 200


def log_prediction_console(log_payload):
    print('logging {}'.format(log_payload))


def log_prediction_fluentd(log_payload):
    logger = sender.FluentSender(
        TENANT, host=FLUENTD_HOST, port=int(FLUENTD_PORT))
    
    if not logger.emit('prediction', log_payload):
        print("Could not log to Fluentd: {}".format(logger.last_error))
        logger.clear_last_error()
