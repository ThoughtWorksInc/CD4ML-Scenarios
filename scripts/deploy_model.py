from cd4ml.deploy_model import deploy_model
from cd4ml.get_problem import get_problem


def main(*args):
    """
    Check model meets acceptance threshold
    """
    args = args[0]
    host_name = args[0]
    problem_name = args[1]
    deploy_model(problem_name, host_name=host_name)
