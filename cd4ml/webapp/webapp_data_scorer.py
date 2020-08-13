import logging

logger = logging.getLogger(__name__)


def form_values_to_input_data(form_data, numeric_cols):
    # apply the right schema
    input_data = {}
    for key, val in form_data.items():
        if key in numeric_cols:
            input_data[key] = val
        else:
            input_data[key] = val

    return input_data


def get_form_from_model(spec_name, identifier, model, initial_values=None):
    omitted_fields = model.feature_set.omitted_feature_fields_for_input()

    if initial_values is not None:
        numerical_fields = model.feature_set.encoded_feature_fields_numerical()
        input_data = form_values_to_input_data(initial_values, numerical_fields)
    else:
        input_data = None

    post_url = f'/{spec_name}/{identifier}'
    header_text, form_div = model.encoder.get_form_html_elements(initial_values=input_data,
                                                                 post_url=post_url,
                                                                 omitted_fields=omitted_fields)

    if input_data is not None:
        prediction = model.predict_single_processed_row(input_data)
    else:
        prediction = ""

    logger.info('prediction {}'.format(prediction))
    return header_text, form_div, prediction
