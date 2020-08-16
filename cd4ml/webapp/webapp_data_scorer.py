import logging

logger = logging.getLogger(__name__)


def get_form_from_model(spec_name, identifier, model, initial_values=None):
    omitted_fields = model.feature_set.omitted_feature_fields_for_input()

    if initial_values is not None:
        input_data = initial_values
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
