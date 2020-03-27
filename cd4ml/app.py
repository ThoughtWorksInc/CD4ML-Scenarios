from flask import Flask, render_template, request
from datetime import datetime
import joblib
import pandas as pd
import os
from fluent import sender
from cd4ml.filenames import file_names

# TODO: needs fixing to work with new data


app = Flask(__name__, template_folder='webapp/templates',
            static_folder='webapp/static')

products = {
    "99197": {
        "class": 1067,
        "family": "GROCERY I",
        "perishable": 0
    },
    "105574": {
        "class": 1045,
        "family": "GROCERY I",
        "perishable": 0
    },
    "1963838": {
        "class": 3024,
        "family": "CLEANING",
        "perishable": 0
    }
}

TENANT = os.getenv('TENANT', 'model')
FLUENTD_HOST = os.getenv('FLUENTD_HOST')
FLUENTD_PORT = os.getenv('FLUENTD_PORT')

print("FLUENTD_HOST="+FLUENTD_HOST)
print("FLUENTD_PORT="+FLUENTD_PORT)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/replacemodel', methods=["POST"])
def replace_model():
    content = request.get_data(as_text=False)
    with open(file_names['model'], 'w+b') as f:
        f.write(content)
    return "OK", 200


@app.route('/prediction')
def get_prediction():
    loaded_model = joblib.load(file_names['model'])

    date_string = request.args.get('date')

    date = datetime.strptime(date_string, '%Y-%m-%d')

    product = products[request.args.get("item_nbr")]
    data = {
        "date": date_string,
        "item_nbr": request.args.get("item_nbr"),
        "family": product['family'],
        "class": product['class'],
        "perishable": product['perishable'],
        "transactions": 1000,
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "dayofweek": date.weekday(),
        "days_til_end_of_data": 0,
        "dayoff": date.weekday() >= 5
    }

    df = pd.DataFrame(data=data, index=['row1'])

    pred = loaded_model.predict(df)
    if FLUENTD_HOST is not None:
        log_payload = {'prediction': pred[0], **data}
        print('logging {}'.format(log_payload))
        logger = sender.FluentSender(
            TENANT, host=FLUENTD_HOST, port=int(FLUENTD_PORT))

        if not logger.emit('prediction', log_payload):
            print(logger.last_error)
            logger.clear_last_error()

    return "%d" % pred[0]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
