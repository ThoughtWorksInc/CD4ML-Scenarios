from pathlib import Path
from cd4ml.filenames import file_names
from cd4ml.model_utils import load_model
from cd4ml.utils import float_or_zero


def form_values_to_input_data(form_data, numeric_cols):
    # apply the right schema
    input_data = {}
    for key, val in form_data.items():
        if key in numeric_cols:
            input_data[key] = float_or_zero(val)
        else:
            input_data[key] = val

    return input_data


def get_form_from_model(initial_values=None):
    if not Path(file_names['full_model']).exists():
        return "ERROR", "Model Not Loaded"

    loaded_model = load_model()

    omitted_fields = loaded_model.feature_set.omitted_feature_fields_for_input()

    if initial_values is not None:
        numerical_fields = loaded_model.feature_set.encoded_feature_fields_numerical()
        input_data = form_values_to_input_data(initial_values, numerical_fields)
    else:
        input_data = None

    del initial_values

    header_text, form_div = loaded_model.encoder.get_form_html_elements(initial_values=input_data,
                                                                        post_url='/',
                                                                        omitted_fields=omitted_fields)

    if input_data is not None:
        prediction = loaded_model.predict_single_processed_row(input_data)
    else:
        prediction = ""

    print('prediction', prediction)
    return header_text, form_div, prediction
