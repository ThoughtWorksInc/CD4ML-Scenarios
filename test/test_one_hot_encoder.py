from cd4ml.one_hot.one_hot_encoder import OneHotEncoder
from tempfile import NamedTemporaryFile


def test_init_empty():
    OneHotEncoder([], [])


def test_init():
    encoder = OneHotEncoder({'foo': 3, 'bar': 7}, ['buzz_numeric'])
    assert encoder.numeric_cols == ['buzz_numeric']
    assert encoder.categorical_n_levels_dict == {'foo': 3, 'bar': 7}


def test_init_ignore_default():
    encoder = OneHotEncoder({'foo': 3, 'bar': 7}, ['buzz_numeric'], max_levels_default=999)
    assert encoder.numeric_cols == ['buzz_numeric']
    assert encoder.categorical_n_levels_dict == {'foo': 3, 'bar': 7}


def test_init_do_not_ignore_default():
    encoder = OneHotEncoder(['foo', 'bar'], ['buzz_numeric'], max_levels_default=999)
    assert encoder.numeric_cols == ['buzz_numeric']
    assert encoder.categorical_n_levels_dict == {'foo': 999, 'bar': 999}


def test_load_from_data():
    encoder = OneHotEncoder(['animal', 'color'], ['weight'], max_levels_default=100)
    data = [{'animal': 'cat', 'color': 'blue', 'weight': 1.0},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 2.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 0.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 99.9}]

    assert encoder.encoder is None
    assert encoder.decoder is None
    assert encoder.one_hot_encoder_dicts is None

    encoder.load_from_data_stream(data)

    assert encoder.encoder is not None
    assert encoder.decoder is not None
    assert encoder.one_hot_encoder_dicts is not None


def test_load_from_data_encodes_data():
    encoder = OneHotEncoder(['animal', 'color'], ['weight'], max_levels_default=100)
    data = [{'animal': 'cat', 'color': 'blue', 'weight': 1.0},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 2.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 0.0},
            {'animal': 'cat', 'color': 'blue', 'weight': 99.9}]

    encoder.load_from_data_stream(data)

    encoded_data = [encoder.encode_row(row) for row in data]
    assert len(encoded_data) == len(data)
    assert len(encoded_data[0]) != len(data[0])


def test_load_from_data_encodes_data_correctly():
    encoder = OneHotEncoder(['animal', 'color'], ['weight'], max_levels_default=100)

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0},
            {'animal': 'mouse', 'color': 'purple', 'weight': 0.0},
            {'animal': 'mouse', 'color': 'black', 'weight': 99.9}]

    encoder.load_from_data_stream(data)

    encoded_data = [encoder.encode_row(row) for row in data]
    assert len(encoded_data) == len(data)
    assert len(encoded_data[0]) != len(data[0])

    first_row = encoded_data[0]

    expected = [6.0,  # weight is numeric and comes first
                1.0,  # animal is first categorical and cat is the most common, first row is cat
                0.0,  # animal, mouse is next most common, not a mouse
                0.0,  # animal, dog and fish tied for frequency but dog first alphabetically
                0.0,  # animal, fish, cat is not a fish
                1.0,  # color is next categorical alphabetically and blue is most common, first row blue
                0.0,  # black
                0.0,  # magenta
                0.0,  # purple
                0.0,  # red
                0.0]  # yellow
    assert first_row == expected

    second_row = encoded_data[1]

    expected = [3.0,  # weight is numeric and comes first
                1.0,  # animal is first categorical and cat is the most common, first row is cat
                0.0,  # animal, mouse is next most common, not a mouse
                0.0,  # animal, dog and fish tied for frequency but dog first alphabetically
                0.0,  # animal, fish, cat is not a fish
                0.0,  # color is next categorical alphabetically and blue is most common, first row blue
                0.0,  # black next alphabetically for ones with frequency 1
                0.0,  # magenta next
                0.0,  # purple
                1.0,  # red, this is red
                0.0]  # yellow
    assert second_row == expected

    last_row = encoded_data[-1]

    expected = [99.9,  # weight is numeric and comes first
                0.0,  # animal is first categorical and cat is the most common, first row is cat
                1.0,  # animal, mouse is next most common, not a mouse
                0.0,  # animal, dog and fish tied for frequency but dog first alphabetically
                0.0,  # animal, fish, cat is not a fish
                0.0,  # color is next categorical alphabetically and blue is most common, first row blue
                1.0,  # black next alphabetically for ones with frequency 1, this one black
                0.0,  # magenta next
                0.0,  # purple
                0.0,  # red
                0.0]  # yellow

    assert last_row == expected

    expected_total = [[6.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                      [5.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                      [7.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                      [99.9, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]]

    assert encoded_data == expected_total


def test_save_load():
    filename = NamedTemporaryFile().name

    encoder = OneHotEncoder(['animal', 'color'], ['weight'], max_levels_default=100)

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0},
            {'animal': 'mouse', 'color': 'purple', 'weight': 0.0},
            {'animal': 'mouse', 'color': 'black', 'weight': 99.9}]

    encoder.load_from_data_stream(data)

    encoded_data = encoder.encode_data(data)

    encoder.save(filename)

    encoder_from_file = OneHotEncoder([], [])
    encoder_from_file.load_from_file(filename)

    encoded_data_from_file = encoder_from_file.encode_data(data)

    assert encoded_data == encoded_data_from_file


def test_inversion():
    encoder = OneHotEncoder(['animal', 'color'], ['weight'], max_levels_default=100)

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0},
            {'animal': 'mouse', 'color': 'purple', 'weight': 0.0},
            {'animal': 'mouse', 'color': 'black', 'weight': 99.9}]

    encoder.load_from_data_stream(data)

    encoded_data = encoder.encode_data(data)

    data_decoded = encoder.decode_data(encoded_data)
    assert data_decoded == data

    data_recoded = encoder.encode_data(data_decoded)
    assert data_recoded == encoded_data


def test_inversion_more_complicated():
    encoder = OneHotEncoder(['animal', 'color'], ['weight', 'height'], max_levels_default=100)

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0, 'height': 88.9},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0, 'height': 44.9},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5, 'height': 2.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0, 'height': 3233.2},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0, 'height': 666.6},
            {'animal': 'mouse', 'color': 'red', 'weight': 0.0, 'height': 55.5},
            {'animal': 'mouse', 'color': 'blah', 'weight': 99.9, 'height': 33}]

    encoder.load_from_data_stream(data)

    encoded_data = encoder.encode_data(data)

    data_decoded = encoder.decode_data(encoded_data)
    assert data_decoded == data

    data_recoded = encoder.encode_data(data_decoded)
    assert data_recoded == encoded_data


def test_inversion_more_complicated_with_max_levels():
    encoder = OneHotEncoder({'animal': 2 , 'color': 2}, ['weight', 'height'])

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0, 'height': 88.9},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0, 'height': 44.9},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5, 'height': 2.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0, 'height': 3233.2},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0, 'height': 666.6},
            {'animal': 'mouse', 'color': 'red', 'weight': 0.0, 'height': 55.5},
            {'animal': 'mouse', 'color': 'blah', 'weight': 99.9, 'height': 33}]

    encoder.load_from_data_stream(data)

    encoded_data = encoder.encode_data(data)
    data_decoded = encoder.decode_data(encoded_data)

    expected = [{'height': 88.9, 'weight': 6.0, 'animal': 'cat', 'color': 'blue'},
                {'height': 44.9, 'weight': 3.0, 'animal': 'cat', 'color': 'red'},
                {'height': 2.5, 'weight': 5.5, 'color': 'UNKNOWN_CATEGORICAL_LEVEL', 'animal': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 3233.2, 'weight': 7.0, 'color': 'blue', 'animal': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 666.6, 'weight': 2.0, 'animal': 'cat', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 55.5, 'weight': 0.0, 'animal': 'mouse', 'color': 'red'},
                {'height': 33, 'weight': 99.9, 'animal': 'mouse', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'}]

    assert data_decoded == expected


def test_inversion_more_complicated_with_max_levels_diff():
    encoder = OneHotEncoder({'animal': 2, 'color': 1}, ['weight', 'height'])

    data = [{'animal': 'cat', 'color': 'blue', 'weight': 6.0, 'height': 88.9, 'extra_junk': 'blah'},
            {'animal': 'cat', 'color': 'red', 'weight': 3.0, 'height': 44.9},
            {'animal': 'dog', 'color': 'yellow', 'weight': 5.5, 'height': 2.5},
            {'animal': 'fish', 'color': 'blue', 'weight': 7.0, 'height': 3233.2},
            {'animal': 'cat', 'color': 'magenta', 'weight': 2.0, 'height': 666.6},
            {'animal': 'mouse', 'color': 'red', 'weight': 0.0, 'height': 55.5},
            {'animal': 'mouse', 'color': 'blah', 'weight': 99.9, 'height': 33}]

    encoder.load_from_data_stream(data)

    encoded_data = encoder.encode_data(data)
    data_decoded = encoder.decode_data(encoded_data)

    expected = [{'height': 88.9, 'weight': 6.0, 'animal': 'cat', 'color': 'blue'},
                {'height': 44.9, 'weight': 3.0, 'animal': 'cat', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 2.5, 'weight': 5.5, 'color': 'UNKNOWN_CATEGORICAL_LEVEL', 'animal': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 3233.2, 'weight': 7.0, 'color': 'blue', 'animal': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 666.6, 'weight': 2.0, 'animal': 'cat', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 55.5, 'weight': 0.0, 'animal': 'mouse', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'},
                {'height': 33, 'weight': 99.9, 'animal': 'mouse', 'color': 'UNKNOWN_CATEGORICAL_LEVEL'}]

    assert data_decoded == expected
