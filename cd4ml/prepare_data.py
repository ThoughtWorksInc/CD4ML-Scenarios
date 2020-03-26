import pandas as pd
from sklearn.preprocessing import LabelEncoder
from cd4ml.filenames import file_names


def load_data():
    filename = file_names['train']
    print("Loading data from {}".format(filename))
    train = pd.read_csv(filename)

    filename = file_names['validation']
    print("Loading data from {}".format(filename))
    validate = pd.read_csv(filename)

    return train, validate


def join_tables(train, validate):
    print("Joining tables for consistent encoding")
    return train.append(validate).drop('date', axis=1)


def get_encoder(df, columns_to_encode):
    encoder = LabelEncoder()
    for col in columns_to_encode:
        encoder.fit(df[col])
    return encoder


def encode_categorical_columns_deprecated(df):
    obj_df = df.select_dtypes(include=['object', 'bool']).copy().fillna('-1')
    lb = LabelEncoder()
    for col in obj_df.columns:
        df[col] = lb.fit_transform(obj_df[col])
    return df


def encode_with_encoder(df, encoder):
    df_encoded = df.copy()
    for col in df.columns:
        df_encoded[col] = encoder.transform(df[col])

    return df_encoded


def get_columns_to_encode():
    return ['item_nbr', 'family', 'class', 'year', 'month', 'dayofweek']


def encode(train, validate):
    print("Encoding categorical variables")
    cols_to_encode = get_columns_to_encode()
    joined = join_tables(train, validate)
    encoder = get_encoder(joined, cols_to_encode)
    # TODO: persist the encoder

    train_encoded = encode_with_encoder(train, encoder)
    validate_encoded = encode_with_encoder(validate, encoder)

    return train_encoded, validate_encoded
