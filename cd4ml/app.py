from flask import Flask, render_template, request
import os
from fluent import sender
from cd4ml.app_utils import replace_model_file, replace_encoder_file

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
    replace_model_file(content)
    return "OK", 200


@app.route('/replace_encoder', methods=["POST"])
def replace_encoder():
    content = request.get_data(as_text=False)
    replace_encoder_file(content)
    return "OK", 200


def log_prediction(pred):
    log_payload = {'prediction': pred}
    print('logging {}'.format(log_payload))
    logger = sender.FluentSender(
        TENANT, host=FLUENTD_HOST, port=int(FLUENTD_PORT))

    if not logger.emit('prediction', log_payload):
        print(logger.last_error)
        logger.clear_last_error()


@app.route('/prediction')
def get_prediction():
    date_string = request.args.get('date')
    item_nbr = request.args.get("item_nbr"),

    pred = get_prediction(item_nbr, date_string)
    log_prediction(pred)

    if FLUENTD_HOST is not None:
        log_prediction(pred)

    return "%d" % pred


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
