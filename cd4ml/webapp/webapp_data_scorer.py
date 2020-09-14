import logging

from cd4ml.utils.utils import float_or_zero

logger = logging.getLogger(__name__)


def form_values_to_input_data(form_data, numeric_cols):
    # apply the right schema
    input_data = {}
    for key, val in form_data.items():
        if key in numeric_cols:
            input_data[key] = float_or_zero(val)
        else:
            input_data[key] = str(val)

    return input_data


def get_form_from_model(spec_name, identifier, model, initial_values=None):
    omitted_fields = model.feature_set.omitted_feature_fields_for_input()

    if initial_values is not None:
        numeric_cols = model.feature_set.ml_fields()['numerical']
        input_data = form_values_to_input_data(initial_values, numeric_cols)
    else:
        input_data = None

    header_text, form_div = model.encoder.get_form_html_elements(initial_values=input_data,
                                                                 post_url=f'/{spec_name}/{identifier}',
                                                                 omitted_fields=omitted_fields)

    if input_data is not None:
        prediction = model.predict_single_processed_row(input_data)
    else:
        prediction = None

    return header_text, form_div, prediction
