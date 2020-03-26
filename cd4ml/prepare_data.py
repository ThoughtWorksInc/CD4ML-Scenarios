from sklearn.preprocessing import LabelEncoder
from cd4ml.filenames import file_names
from cd4ml.read_data import read_raw_data, transform_data


def load_data():
    filename = file_names['train']
    print("Loading data from {}".format(filename))
    train = read_raw_data(filename)

    filename = file_names['validation']
    print("Loading data from {}".format(filename))
    validate = read_raw_data(filename)

    transform_data(train)
    transform_data(validate)

    return train, validate


def join_tables(train, validate):
    print("Joining tables for consistent encoding")
    return train.append(validate)


def get_encoders(df, columns_to_encode):
    # df = df.select_dtypes(include=['object', 'bool']).copy().fillna('-1')
    print('Encoding')
    encoders = {}
    for col in columns_to_encode:
        encoders[col] = LabelEncoder()
        encoders[col].fit(df[col])
    print('Done encoding')
    return encoders


def encode_with_encoders(df, encoders, columns_to_encode):
    df_encoded = df.copy()
    for col in columns_to_encode:
        print('column being encoded', col)
        df_encoded[col] = encoders[col].transform(df[col])

    return df_encoded


def get_columns_to_encode():
    return ['item_nbr', 'family', 'class', 'year', 'month', 'dayofweek']


def encode(train, validate):
    print("Encoding categorical variables")
    cols_to_encode = get_columns_to_encode()
    joined = join_tables(train, validate)
    encoders = get_encoders(joined, cols_to_encode)
    # TODO: persist the encoders

    print('Encoding train')
    train_encoded = encode_with_encoders(train, encoders, cols_to_encode)
    print('Encoding validate')
    validate_encoded = encode_with_encoders(validate, encoders, cols_to_encode)

    return train_encoded, validate_encoded
