import json
from cd4ml.problems.available_problems import PROBLEMS


def read_schema_file(schema_file):
    schema = read_json_file_as_dict(schema_file)
    # Verify the file before processing
    categorical_fields = schema['categorical']
    numeric_fields = schema['numerical']

    # Make sure the same field is not in both categorical and numerical sections
    overlap = set(categorical_fields).intersection(numeric_fields)
    if len(overlap) != 0:
        error = "The field(s) {} is contained in both the categorical and numeric fields. " \
                "Please check the file and re-run the application.".format(overlap)
        raise ValueError(error)

    return categorical_fields, numeric_fields


def read_json_file_as_dict(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def list_available_scenarios():
    return list(PROBLEMS.keys())


def get_problem(problem_name,
                data_downloader='default',
                ml_pipeline_params_name='default',
                feature_set_name='default',
                algorithm_name='default',
                algorithm_params_name='default'):
    constructor_object = PROBLEMS.get(problem_name)
    return constructor_object(problem_name,
                              data_downloader,
                              ml_pipeline_params_name,
                              feature_set_name,
                              algorithm_name,
                              algorithm_params_name)
