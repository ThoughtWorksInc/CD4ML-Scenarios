from cd4ml.one_hot import one_hot_encode as ohe
import json


class OneHotEncoder:
    def __init__(self, categorical_cols, numeric_cols, max_levels_default=10000):
        assert max_levels_default > 0
        self.max_levels_default = max_levels_default
        self.numeric_cols = numeric_cols
        self.one_hot_encoder_dicts = None
        self.encoder = None
        self.decoder = None
        self.index_lookup = None
        if isinstance(categorical_cols, list):
            self.categorical_n_levels_dict = {k: self.max_levels_default for k in categorical_cols}
        elif isinstance(categorical_cols, dict):
            assert min(list(categorical_cols.values())) > 0
            self.categorical_n_levels_dict = categorical_cols
        else:
            raise ValueError('categorical_cols must be a list or dictionary')

    def load_from_data_stream(self, stream_of_dicts):
        self.one_hot_encoder_dicts = ohe.get_one_hot_encoder_dicts_from_data_stream(stream_of_dicts,
                                                                                    self.categorical_n_levels_dict)
        self._get_encoder_decoder()

    def _package_data(self):
        data = {'max_levels_default': self.max_levels_default,
                'numeric_cols': self.numeric_cols,
                'categorical_n_levels_dict': self.categorical_n_levels_dict,
                'one_hot_encoder_dicts': self.one_hot_encoder_dicts}
        return data

    def save(self, json_file_name):
        with open(json_file_name, 'w') as fp:
            json.dump(self._package_data(), fp)

    def load_from_file(self, json_file_name):
        with open(json_file_name, 'r') as fp:
            data = json.load(fp)
            self.max_levels_default = data['max_levels_default']
            self.numeric_cols = data['numeric_cols']
            self.one_hot_encoder_dicts = data['one_hot_encoder_dicts']

        self._get_encoder_decoder()

    def _get_encoder_decoder(self):
        self.index_lookup = ohe.get_key_val_pair_to_index_lookup(self.one_hot_encoder_dicts, self.numeric_cols)
        self.index_lookup_rev = {v: k for k, v in self.index_lookup.items()}
        self.encoder, self.decoder = ohe.get_line_encoder_and_decoder(self.index_lookup)

    def encode_row(self, row):
        return self.encoder(row)

    def decode_row(self, row):
        return self.decoder(row)

    def index_to_column(self, index):
        return self.index_lookup_rev[index]

    def get_index(self, x):
        if isinstance(x, tuple):
            key, value = x
        elif isinstance(x, str):
            key = x
            value = None
        else:
            raise ValueError('x must be a string for numeric col of key value pair for categorical level')

        idx, _ = ohe.get_index(key, value, self.index_lookup)
        return idx

    def encode_data_stream(self, stream):
        # generator
        return (self.encode_row(row) for row in stream)

    def encode_data(self, stream):
        return list(self.encode_data_stream(stream))

    def decode_data_stream(self, encoded_data_stream):
        return (self.decode_row(row) for row in encoded_data_stream)

    def decode_data(self, encoded_data_stream):
        return list(self.decode_data_stream(encoded_data_stream))
