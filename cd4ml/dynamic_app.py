from pathlib import Path
import joblib
from cd4ml.filenames import file_names
from cd4ml.get_problem import get_problem


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

    # TODO, remove these hard coded values and get from the right place
    omitted_fields = ['sale_id',
                      'state',
                      'avg_price_in_zip',
                      'num_in_zip']

    header_text, form_div = encoder.get_form_html_elements(initial_values=initial_values,
                                                           post_url='/',
                                                           omitted_fields=omitted_fields)

    if initial_values is not None:
        problem = get_problem()
        features = problem.feature_set.features(initial_values)
        prediction = loaded_model.predict_row(features)
    else:
        prediction = ""

    return header_text, form_div, prediction
