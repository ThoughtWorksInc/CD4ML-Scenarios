from pathlib import Path
import joblib
from wickedhot.form_generator import generate_form
from cd4ml.filenames import file_names


def get_form_from_model():
    if not Path(file_names['full_model']).exists():
        return "ERROR", "Model Not Loaded"

    loaded_model = joblib.load(file_names['full_model'])
    encoder = loaded_model.encoder
    package = encoder.package_data()

    form = generate_form(package)
    return form
