from cd4ml.read_data import process, stream_raw_data, stream_data, get_encoder_from_stream
from cd4ml.one_hot.one_hot_encoder import OneHotEncoder


def test_stream_raw_data():
    stream = stream_raw_data()
    row = next(stream)
    assert isinstance(row, dict)
    assert 'transactions' in row
    assert isinstance(row['transactions'], str)


def test_stream_data():
    stream = stream_data()
    row = next(stream)
    assert isinstance(row, dict)
    assert 'transactions' in row
    assert isinstance(row['transactions'], int)


def test_process():
    row_in = {'id': '88219279',
              'date': '2016-08-16',
              'item_nbr': '103520',
              'unit_sales': '10.0',
              'family': 'GROCERY I',
              'class': '1028',
              'perishable': '0',
              'transactions': '3570',
              'year': '2016',
              'month': '8',
              'day': '16',
              'dayofweek': '1',
              'days_til_end_of_data': '364',
              'dayoff': 'False'}

    row = process(row_in)
    expected = {'id': '88219279',
                'item_nbr': '103520',
                'unit_sales': 10.0,
                'date': '2016-08-16',
                'year': '2016',
                'month': '8',
                'day': '16',
                'class': '1028',
                'family': 'GROCERY I',
                'perishable': 0,
                'transactions': 3570,
                'dayofweek': '1',
                'days_til_end_of_data': 364,
                'dayoff': 0}

    assert row == expected


def test_get_encoder_from_stream():
    stream = stream_data()
    stream_small = (next(stream) for _ in range(100))
    encoder = get_encoder_from_stream(stream_small)
    assert isinstance(encoder, OneHotEncoder)

    stream = stream_data()
    stream_small = (next(stream) for _ in range(100))
    encoded = list(encoder.encode_data_stream(stream_small))
    assert len(encoded) == 100

    row_in = {'id': '88219279',
              'date': '2016-08-16',
              'item_nbr': '103520',
              'unit_sales': '10.0',
              'family': 'GROCERY I',
              'class': '1028',
              'perishable': '0',
              'transactions': '3570',
              'year': '2016',
              'month': '8',
              'day': '16',
              'dayofweek': '1',
              'days_til_end_of_data': '364',
              'dayoff': 'False'}

    encoded = encoder.encode_data([row_in])
    decoded = encoder.decode_data(encoded)

    print(decoded[0].keys())
    print(row_in.keys())
    del row_in['date'], row_in['id'], row_in['unit_sales']

    assert decoded[0].keys() == row_in.keys()

    #  make a level not seen
    row_in['class'] = 'FOO'

    encoded = encoder.encode_data([row_in])
    decoded = encoder.decode_data(encoded)

    print(decoded[0].keys())
    print(row_in.keys())

    assert decoded[0].keys() == row_in.keys()
    print(decoded)
    assert decoded[0]['class'] == 'UNKNOWN_CATEGORICAL_LEVEL'
