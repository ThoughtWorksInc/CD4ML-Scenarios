from pathlib import Path
import joblib
from wickedhot.form_generator import generate_form
from cd4ml.filenames import file_names


def load_model():
    loaded_model = joblib.load(file_names['full_model'])
    loaded_model.load_encoder_from_package()
    return loaded_model


def get_form_from_model():
    if not Path(file_names['full_model']).exists():
        return "ERROR", "Model Not Loaded"

    loaded_model = load_model()
    encoder = loaded_model.encoder
    assert encoder is not None

    package = encoder.package_data()

    form = generate_form(package)
    return form
