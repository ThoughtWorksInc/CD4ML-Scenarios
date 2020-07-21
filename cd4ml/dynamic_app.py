from pathlib import Path
from cd4ml.filenames import file_names
from cd4ml.model_utils import load_model


def get_form_from_model(initial_values=None):
    if not Path(file_names['full_model']).exists():
        return "ERROR", "Model Not Loaded"

    loaded_model = load_model()

    # TODO, remove these hard coded values and get from the right place
    omitted_fields = ['sale_id',
                      'state',
                      'avg_price_in_zip',
                      'num_in_zip']

    header_text, form_div = loaded_model.encoder.get_form_html_elements(initial_values=initial_values,
                                                                        post_url='/',
                                                                        omitted_fields=omitted_fields)

    if initial_values is not None:
        initial_values = dict(initial_values)
        prediction = loaded_model.predict_single_processed_row(initial_values)
    else:
        prediction = ""

    print('prediction', prediction)
    return header_text, form_div, prediction
