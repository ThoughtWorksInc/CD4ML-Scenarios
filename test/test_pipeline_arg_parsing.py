from scripts import pipeline as pipeline_script

def test_no_arguments_parse():
    argument_parser = pipeline_script.make_argument_parser()
    parsed_arguments = argument_parser.parse_args([])
    assert parsed_arguments.problem_name == "houses"
    assert parsed_arguments.ml_pipeline_params_name == "default"
    assert parsed_arguments.feature_set_name == "default"
    assert parsed_arguments.algorithm_name == "default"
    assert parsed_arguments.algorithm_params_name == "default"


def test_problem_name_supplied():
    argument_parser = pipeline_script.make_argument_parser()
    parsed_arguments = argument_parser.parse_args(["groceries"])
    assert parsed_arguments.problem_name == "groceries"
    assert parsed_arguments.ml_pipeline_params_name == "default"
    assert parsed_arguments.feature_set_name == "default"
    assert parsed_arguments.algorithm_name == "default"
    assert parsed_arguments.algorithm_params_name == "default"

def test_all_argument_supplied():
    argument_parser = pipeline_script.make_argument_parser()
    parsed_arguments = argument_parser.parse_args(["groceries", "a", "b", "c", "d"])
    assert parsed_arguments.problem_name == "groceries"
    assert parsed_arguments.ml_pipeline_params_name == "a"
    assert parsed_arguments.feature_set_name == "b"
    assert parsed_arguments.algorithm_name == "c"
    assert parsed_arguments.algorithm_params_name == "d"

