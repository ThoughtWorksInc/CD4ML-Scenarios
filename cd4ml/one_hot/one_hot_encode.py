from collections import Counter

unknown_level_value = 'UNKNOWN_CATEGORICAL_LEVEL'


def one_hot_encode_column(data_stream, max_levels):
    count = Counter()
    for value in data_stream:
        count[value] += 1

    most_common = count.most_common()[0:max_levels-1]
    encoder_dict = {}
    i = 1
    for val, num in most_common:
        encoder_dict[val] = i
        i += 1


def select_counter(counter, n_max):
    # first by frequency (largest), then alphabetical by key
    return sorted(counter.most_common(), key=lambda x: (-x[1], x[0]))[0:n_max]


def get_one_hot_encoder_dicts_from_data_stream(stream_of_dicts, categorical_n_levels_dict):
    """
    :param stream_of_dicts: a stream of dictionaries (e.g from csv.DictReader)
    :param categorical_n_levels_dict: dictionary mapping categorical keys to
        maximum number of levels
    :return: dict of dicts. Maps [key][val] to an an index from 0 to max levels +1
            The number of 0 corresponds to either an uncommon level or unseen level
            which are treated the same.
    """
    # data stream is a stream of dictionaries as if from csv.DictReader
    keys = categorical_n_levels_dict.keys()
    count = {k: Counter() for k in keys}
    for row in stream_of_dicts:
        for k in keys:
            count[k][row[k]] += 1

    most_commons = {k: select_counter(count[k], n_max) for k, n_max in categorical_n_levels_dict.items()}
    return {k: {val[0]: i for i, val in enumerate(most_commons[k])} for k in keys}


def get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys):
    encoded_keys = sorted(encoder_dict.keys())
    non_enc_keys = sorted(non_encoded_keys)

    index = {k: i for i, k in enumerate(non_enc_keys)}

    first = len(non_enc_keys)
    for key in encoded_keys:
        n = len(encoder_dict[key])
        for val, idx in encoder_dict[key].items():
            pair = (key, val)
            index[pair] = idx + first
        first += n

    return index


def get_index(key, val, index_lookup):
    idx = None
    encoded_value = None

    if key in index_lookup:
        # non-encoded
        idx = index_lookup[key]
        encoded_value = val

    if (key, val) in index_lookup:
        assert key not in index_lookup
        # one-hot-encoded
        idx = index_lookup[(key, val)]
        encoded_value = 1.0

    return idx, encoded_value


def get_line_encoder_and_decoder(index):
    n_index = len(index)
    all_cols = get_all_cols(index)
    rev_index = {v: k for k, v in index.items()}
    assert len(rev_index) == n_index

    def encoder(line):
        encoded_line = [0.0] * n_index
        for k, v in line.items():
            idx, encoded_value = get_index(k, v, index)
            if idx is not None:
                encoded_line[idx] = encoded_value

        return encoded_line

    def decoder(encoded_line):
        assert len(encoded_line) == n_index
        decoded_line = {}
        for idx, val in enumerate(encoded_line):
            value = rev_index[idx]

            if isinstance(value, tuple):
                assert val == 1.0 or val == 0.0
                if val == 1.0:
                    assert value[0] not in decoded_line
                    decoded_line[value[0]] = value[1]

            elif isinstance(value, str):
                decoded_line[value] = val

        fill_in_unknown_levels(decoded_line, all_cols)
        return decoded_line

    return encoder, decoder


def get_all_cols(index):
    all_cols = set()
    for k in index.keys():
        if isinstance(k, str):
            all_cols.add(k)
        if isinstance(k, tuple):
            all_cols.add(k[0])
    return all_cols


def fill_in_unknown_levels(decoded_line, all_cols):
    for k in all_cols:
        if k not in decoded_line:
            decoded_line[k] = unknown_level_value
