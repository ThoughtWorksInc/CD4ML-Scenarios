from pathlib import Path
import joblib
from cd4ml.filenames import file_names
from cd4ml.get_problem import get_problem


def get_omits_and_extras(encoder):
    problem = get_problem()
    params = problem.feature_set.params

    base_cat = list(params['base_categorical_n_levels_dict'].keys())
    base_num = params['base_numeric_fields']
    base_features = base_num + base_cat

    retained_fields = params['base_features_numerical_retain'] + \
        params['base_features_categorical_retain']

    encoder_numeric = encoder.numeric_cols
    encoder_cat = list(encoder.one_hot_encoder_dicts.keys())
    encoder_features = encoder_numeric + encoder_cat

    omitted_fields = [field for field in encoder_features if field not in base_features]

    extra_numeric = [field for field in base_num if field not in encoder_features]
    extra_cat = [field for field in base_cat if field not in encoder_features]


def load_model():
    loaded_model = joblib.load(file_names['full_model'])
    loaded_model.load_encoder_from_package()
    return loaded_model


def get_form_from_model(initial_values=None):
    if not Path(file_names['full_model']).exists():
        return "ERROR", "Model Not Loaded"

    loaded_model = load_model()
    encoder = loaded_model.encoder
    assert encoder is not None

    header_text, form_div = encoder.get_form_html_elements(initial_values=initial_values,
                                                           post_url='/')

    if initial_values is not None:
        prediction = loaded_model.predict_row(initial_values)
    else:
        prediction = ""

    return header_text, form_div, prediction
