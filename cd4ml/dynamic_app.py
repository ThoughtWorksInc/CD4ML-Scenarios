from pathlib import Path
from cd4ml.filenames import get_filenames
from cd4ml.model_utils import load_deployed_model
from cd4ml.utils import float_or_zero
from glob import glob
import os


def form_values_to_input_data(form_data, numeric_cols):
    # apply the right schema
    input_data = {}
    for key, val in form_data.items():
        if key in numeric_cols:
            input_data[key] = float_or_zero(val)
        else:
            input_data[key] = val

    return input_data


def get_form_from_model(spec_name, initial_values=None):
    problem_name = spec_name.split('$')[0]
    file_names = get_filenames(problem_name, problem_specification_name=spec_name)
    if not Path(file_names['full_model_deployed']).exists():
        return "ERROR", "Model Not Loaded", None

    loaded_model = load_deployed_model(spec_name)

    omitted_fields = loaded_model.feature_set.omitted_feature_fields_for_input()

    if initial_values is not None:
        numerical_fields = loaded_model.feature_set.encoded_feature_fields_numerical()
        input_data = form_values_to_input_data(initial_values, numerical_fields)
    else:
        input_data = None

    post_url = '/%s' % spec_name
    header_text, form_div = loaded_model.encoder.get_form_html_elements(initial_values=input_data,
                                                                        post_url=post_url,
                                                                        omitted_fields=omitted_fields)

    if input_data is not None:
        prediction = loaded_model.predict_single_processed_row(input_data)
    else:
        prediction = ""

    print('prediction', prediction)
    return header_text, form_div, prediction


def list_available_models():
    from cd4ml.filenames import data_dir
    results_dir = data_dir + '/results'
    specs = glob(results_dir+'/*')
    available_specs = []
    for spec in specs:
        print(spec)
        if os.path.exists("%s/%s" % (spec, 'full_model_deployed.pkl')):
            available_specs.append(spec.split('results/')[-1])

    return available_specs
