from pathlib import Path
import joblib
from cd4ml.filenames import file_names


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

    form = encoder.get_form_html_page(initial_values=initial_values, post_url='/dynamic')
    return form
