# parameters for running the pipeline
import yaml
from cd4ml.filenames import file_names


def get_pipeline_config():
    filename = file_names['pipeline_config']
    return yaml.safe_load(open(filename, 'r'))


def get_problem():
    pipeline_config = get_pipeline_config()
    problem_name = pipeline_config['problem_name']

    if problem_name == 'groceries':
        from cd4ml.problems.groceries.problem import GroceriesProblem as Problem
    elif problem_name == 'houses':
        from cd4ml.problems.houses.problem import HousesProblem as Problem
    else:
        raise ValueError('Problem name: %s unknown' % problem_name)

    return Problem()
