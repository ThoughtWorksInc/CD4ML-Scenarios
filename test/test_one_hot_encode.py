from cd4ml.one_hot import one_hot_encode as ohe


def test_get_one_hot_encoder_dicts_from_data_stream_with_ties():
    data = [{'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'a', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'b', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'b', 'animal': 'dog', 'color': 'blue'},
            {'letter': 'b', 'animal': 'cat', 'color': 'green'}]

    stream = (i for i in data)

    categorical_n_levels_dict = {'letter': 1, 'animal': 1, 'color': 2}

    encoders = ohe.get_one_hot_encoder_dicts_from_data_stream(stream, categorical_n_levels_dict)

    expected = {'letter': {'a': 0},
                'animal': {'cat': 0},
                'color': {'blue': 0, 'red': 1}}

    assert encoders == expected


def test_get_key_val_pair_to_index_lookup_simple():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = []
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)

    expected = {('animal', 'cat'): 0,
                ('color', 'blue'): 1,
                ('color', 'red'): 2,
                ('letter', 'a'): 3}

    assert index == expected


def test_get_key_val_pair_to_index_lookup_simple_with_numeric():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = ['blah']
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)

    expected = {'blah': 0,
                ('animal', 'cat'): 1,
                ('color', 'blue'): 2,
                ('color', 'red'): 3,
                ('letter', 'a'): 4}

    assert index == expected


def test_get_line_encoder_and_decoder():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = []
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)
    e, d = ohe.get_line_encoder_and_decoder(index)

    line = {'letter': 'a', 'animal': 'cat', 'color': 'blue'}
    encoded_line = e(line)
    expected = [1.0, 1.0, 0.0, 1.0]

    assert encoded_line == expected

    decoded_line = d(encoded_line)
    assert decoded_line == line


def test_get_line_encoder_and_decoder_with_numerics():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = ['foo', 'bar']
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)
    e, d = ohe.get_line_encoder_and_decoder(index)

    line = {'foo': 88.0, 'letter': 'a', 'animal': 'cat', 'color': 'blue', 'bar': 5.5}
    encoded_line = e(line)
    expected = [5.5, 88.0, 1.0, 1.0, 0.0, 1.0]

    assert encoded_line == expected

    decoded_line = d(encoded_line)
    assert decoded_line == line


def test_get_one_hot_encoder_dicts_from_data_stream():
    data = [{'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'b', 'animal': 'dog', 'color': 'red'},
            {'letter': 'b', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'c', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'a', 'animal': 'dog', 'color': 'blue'},
            {'letter': 'a', 'animal': 'mouse', 'color': 'green'}]

    stream = (i for i in data)

    categorical_n_levels_dict = {'letter': 2, 'animal': 5, 'color': 2}

    encoders = ohe.get_one_hot_encoder_dicts_from_data_stream(stream, categorical_n_levels_dict)

    expected = {'letter': {'a': 0, 'b': 1},
                'animal': {'dog': 0, 'cat': 1, 'mouse': 2},
                'color': {'blue': 0, 'red': 1}}

    assert encoders == expected
