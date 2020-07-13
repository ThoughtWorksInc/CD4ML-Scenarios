import joblib
from cd4ml.filenames import file_names
from cd4ml.date_utils import date_string_to_weekday
from cd4ml.read_data import get_encoder, process
from pathlib import Path

products = {
    "99197": {
        "class": '1067',
        "family": 'GROCERY I',
        "perishable": '0'
    },
    "105574": {
        "class": '1045',
        "family": 'GROCERY I',
        "perishable": 0
    },
    "1963838": {
        "class": '3024',
        "family": 'CLEANING',
        "perishable": 0
    }
}

product_name_map = {
    "99197": "Milk",
    "105574": "Cheese",
    "1963838": "Soap"
}


def get_product_name_from_id(id):
    return product_name_map.get(id)


def get_processed_row(item_nbr, date_string):
    ymd = date_string.split('-')
    ymd = [int(i) for i in ymd]
    year, month, day = ymd

    weekday = date_string_to_weekday(date_string)
    # TODO: calculate this
    days_til_end_of_data = 0

    product = products[item_nbr]

    raw_row = {
        "date": date_string,
        "item_nbr": item_nbr,
        "family": product['family'],
        "class": product['class'],
        "perishable": product['perishable'],
        "year": str(year),
        "month": str(month),
        "day": str(day),
        "dayofweek": str(weekday),
        "days_til_end_of_data": days_til_end_of_data,
        "dayoff": str(weekday >= 5),
        "unit_sales": '0'
    }

    row = process(raw_row)

    return row


def get_encoded_row(item_nbr, date_string, encoder):
    processed_row = get_processed_row(item_nbr, date_string)
    encoded_row = encoder.encode_row(processed_row)
    return encoded_row


def replace_model_file(content):
    with open(file_names['model'], 'w+b') as f:
        f.write(content)


def replace_encoder_file(content):
    with open(file_names['encoder'], 'w+b') as f:
        f.write(content)


def get_prediction(item_nbr, date_string):
    if not Path(file_names['model']).exists():
        return "ERROR", "Model Not Loaded"

    if not Path(file_names['encoder']).exists():
        return "ERROR", "Encoder Not Loaded"

    loaded_model = joblib.load(file_names['model'])

    # pipeline_params not needed if reading from file
    pipeline_params = None

    encoder = get_encoder(pipeline_params, read_from_file=True)
    encoded_data = [get_encoded_row(item_nbr, date_string, encoder)]
    return "OK", loaded_model.predict(encoded_data)[0]
