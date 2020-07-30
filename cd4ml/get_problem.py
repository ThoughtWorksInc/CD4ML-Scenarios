# parameters for running the pipeline
import yaml
from cd4ml.filenames import config_file


def get_pipeline_config():
    filename = config_file
    return yaml.safe_load(open(filename, 'r'))


def get_problem(problem_name,
                feature_set_name='default',
                problem_params_name='default',
                algorithm_name='default',
                ml_params_name='default'):

    if problem_name == 'groceries':
        from cd4ml.problems.groceries.problem import GroceriesProblem as Problem
    elif problem_name == 'houses':
        from cd4ml.problems.houses.problem import HousesProblem as Problem
    elif problem_name == 'houses_alt':
        from cd4ml.problems.houses_alt.problem import HousesProblemAlt as Problem
    else:
        raise ValueError('Problem name: %s unknown' % problem_name)

    return Problem(feature_set_name=feature_set_name)
